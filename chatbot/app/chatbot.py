from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# from chatterbot.utils import nltk_download

# nltk_download('punkt')  # Download required NLTK resources (comment out if already downloaded)

chatbot = ChatBot("Bantubot")
trainer = ListTrainer(chatbot)
conversations = []
questions = []

exit_conditions = (":q", "quit", "exit")

def add_conv(question, reply):
    trainer.train([
        question,
        reply,
    ])
    conv = {'question': question, 'reply': reply},
    conversations.append(conv)
    questions.append(question.lower())



# Load initial training data (optional, uncomment if you have initial conversations)
# INITIAL_CORPUS = [
#     ("Hi", "Hi how can I help you "),
#     ("Are you a plant?", "No, I'm the pot below the plant!"),
# ]
# trainer.train(INITIAL_CORPUS)