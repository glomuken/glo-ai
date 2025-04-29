# bot.py

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from cleaner import clean_corpus


chatbot = ChatBot("Bantubot")
queries=[]

# CORPUS_FILE = "chat.txt"

trainer = ListTrainer(chatbot)
# cleaned_corpus = clean_corpus(CORPUS_FILE)
# trainer.train(cleaned_corpus)
trainer.train([
    "Hi",
    "Hi how can I help you 🤗",
])
queries.append(("Hi").lower())
trainer.train([
    "Are you a plant?",
    "No, I'm the pot below the plant!",
])
queries.append(("Are you a plant?").lower())
exit_conditions = (":q", "quit", "exit")

def add_conv(question,reply):
    trainer.train([
        question,
        reply,
    ])
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        if query.lower() in queries:
            print(f"🪴 {chatbot.get_response(query)}")
        else:
            print("🪴I'm sorry, I don't understand that. Please ask me something else.")
