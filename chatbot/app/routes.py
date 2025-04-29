from flask import Flask, render_template, request, jsonify
from cleaner import clean_corpus
from chatbot import chatbot, exit_conditions, add_conv, conversations, trainer,questions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

# Load chatbot instance from chatbot.py
chatbot = chatbot  # Assuming chatbot is defined in chatbot.py

@app.route('/chat', methods=['POST'])
def chat():
    query = request.get_json().get('message')
    if query in exit_conditions:
        return jsonify({'message': 'Goodbye!'})
    else:
        if query.lower() in questions:
            response = chatbot.get_response(query)
        else:
            response = "I'm sorry, I don't understand that. Please ask me something else."
        return jsonify({'message': str(response)})

@app.route('/conversations', methods=['GET'])
def conversations():
    
    return jsonify(conversations)
         
         
@app.route('/add_conversation', methods=['GET', 'POST'])
def add_conversation():
    if request.method == 'POST':
        question = request.form['question']
        reply = request.form['reply']
        add_conv(question, reply)
        return render_template('add_conversation.html', message='Conversation added successfully!')
    else:
        return render_template('add_conversation.html')

@app.route('/upload_chat', methods=['GET', 'POST'])
def upload_chat():
    if request.method == 'POST':
        chat_file = request.files['chat_file']
        cleaned_corpus = clean_corpus(chat_file)
        for question, reply in cleaned_corpus:
            add_conv(question, reply)
        return render_template('upload_chat.html', message='Chat data uploaded and processed successfully!')
    else:
        return render_template('upload_chat.html')

# @app.route('/conversations', methods=['GET'])
# def conversations():
#     return jsonify(conversations)

@app.route('/edit_conversation/<int:conversation_id>', methods=['GET', 'POST'])
def edit_conversation(conversation_id):
    if conversation_id < 0 or conversation_id >= len(conversations):
        return jsonify({'error': 'Invalid conversation ID'}), 400

    conversation = conversations[conversation_id]
    if request.method == 'POST':
        new_question = request.form['question']
        new_reply = request.form['reply']
        conversations[conversation_id] = {'question': new_question, 'reply': new_reply}
        # Retrain the chatbot with the updated conversation
        trainer.train([[new_question, new_reply]])
        return jsonify({'message': 'Conversation updated successfully!'})
    else:
        return render_template('edit_conversation.html', conversation=conversation)
    
@app.route('/delete_conversation/<int:conversation_id>', methods=['POST'])
def delete_conversation(conversation_id):
    if conversation_id < 0 or conversation_id >= len(conversations):
        return jsonify({'error': 'Invalid conversation ID'}), 400

    del conversations[conversation_id]
    # Retrain the chatbot to remove the deleted conversation
    trainer.train(conversations)
    return jsonify({'message': 'Conversation deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)