from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import os

# Const strings
bot_display_name = 'Serwis sklepu internetowego'
user_display_name = 'Użytkownik'
bot_low_confidence_answer = 'Przepraszam ale nie jestem w stanie odpowiedzieć na to pytanie.'
bot_greetings = 'Witam! Jak mogę pomóc?'
bot_bye_answer = 'Do widzenia. Dziękujemy za skorzystanie z naszych usług i zapraszamy ponownie!'
bye_words = ['do widzenia', 'żegnam', 'zegnam', 'koniec']

# Create chatbot, initialize logic adapters and filters
bot = ChatBot(
        'Chatbot',
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparision_function": "chatterbot.comparision.levenstein_distance",
                "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.40,
                'default_response': bot_low_confidence_answer
            }
        ],
        filters=["chatterbot.filters.RepetitiveResponseFilter"]
)

# Train bot from files
bot.set_trainer(ListTrainer)
for _file in os.listdir('train_files'):
    chats = open('train_files/' + _file, 'r').readlines()
    bot.train(chats)

# Train bot with corpus
# bot.set_trainer(ChatterBotCorpusTrainer)
# bot.train("chatterbot.corpus.english.greetings") # test train from coprups english.greetings

continue_dialogue = True

# Start of the conversation
print('{0}: {1}'.format(bot_display_name, bot_greetings))
# Converastion loop
while continue_dialogue:

    # Get input from user
    request = input('{0}: '.format(user_display_name))

    # Check if conversation ends or continues
    continue_dialogue = True
    for bye_word in bye_words:
        if bye_word in request.lower():
            continue_dialogue = False

    # Display chatbot response
    if continue_dialogue:
        response = bot.get_response(request)
        print('{0}: {1} ({2})'.format(bot_display_name, response, response.confidence))
    else:
        print('{0}: {1}'.format(bot_display_name, bot_bye_answer))
