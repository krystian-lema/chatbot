from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import os

# Create chatbot, initialize logic adapters and filters
bot = ChatBot(
        'Chatbot',
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter",
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparision_function": "chatterbot.comparision.levenstein_distance",
                "response_selection_method": "chatterbot.response_selection.get_first_response"
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.40,
                'default_response': 'I am sorry, but I do not understand.'
            }
        ],
        filters=["chatterbot.filters.RepetitiveResponseFilter"]
)

# Train bot from files
bot.set_trainer(ListTrainer)
for _file in os.listdir('train_files'):
    chats = open('files/' + _file, 'r').readlines()
    bot.train(chats)

# Train bot with corpus
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("chatterbot.corpus.english.greetings") # test train from coprups english.greetings

# Words to end up a conversation
bye_words = ['bye', 'Bye']
continue_dialogue = True

# Start of the conversation
print('Bot: Hello! How can I help you?')
# Converastion loop
while continue_dialogue:

    # Get input from user
    request = input('You: ')

    # Check if conversation ends or continues
    continue_dialogue = True
    for bye_word in bye_words:
        if bye_word in request:
            continue_dialogue = False

    # Display chatbot response
    if continue_dialogue:
        response = bot.get_response(request)
        print('Bot: {0} ({1} confidence)'.format(response, response.confidence))
    else:
        print('Bot: Bye bye. It was pleasure to talk with you.')
