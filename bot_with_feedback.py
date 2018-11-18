from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from chatterbot import ChatBot
import os


# Basic configuration
TRAINING = False
ANSWER_CONFIRMATION = True

bot_display_name = 'Serwis sklepu internetowego'
user_display_name = 'Użytkownik'
bot_low_confidence_answer = 'Przepraszam ale nie jestem w stanie odpowiedzieć na to pytanie.'
bot_greetings = 'Witam! Jak mogę pomóc?'
bot_bye_answer = 'Do widzenia. Dziękujemy za skorzystanie z naszych usług i zapraszamy ponownie!'
bye_words = ['do widzenia', 'żegnam', 'zegnam', 'koniec']

CONVERSATION = 'example_feedback_conversation'
CORRECT_ANSWER_CONFIRMATION = 'tak'
INCORRECT_ANSWER_CONFIRMATION = 'nie'

# Create a new instance of a ChatBot
bot = ChatBot(
    'Feedback Learning Bot',
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
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter'
)

def train_bot():
    bot.set_trainer(ListTrainer)
    for _file in os.listdir('train_files'):
        chats = open('train_files/' + _file, 'r').readlines()
        bot.train(chats)

def learn_if_response_is_correct(response, input_statement):
    print('Czy "{}" jest prawidłową odpowiedzią na "{}"?'.format(response, input_statement))

    if get_feedback():
        bot.learn_response(response, input_statement)

def get_feedback():

    text = input()

    if CORRECT_ANSWER_CONFIRMATION in text.lower():
        return True
    elif INCORRECT_ANSWER_CONFIRMATION in text.lower():
        return False
    else:
        print('Odpowiedz ' + CORRECT_ANSWER_CONFIRMATION +  ' lub ' + INCORRECT_ANSWER_CONFIRMATION)
        return get_feedback()

train_bot if TRAINING else False
continue_dialogue = True

print('{0}: {1}'.format(bot_display_name, bot_greetings))

while continue_dialogue:
    try:
        request = input(user_display_name + ": ")
        input_statement = Statement(request)

        continue_dialogue = True
        for bye_word in bye_words:
            if bye_word in request.lower():
                continue_dialogue = False

        if continue_dialogue:
            statement, response = bot.generate_response(
                input_statement,
                CONVERSATION
            )

            learn_if_response_is_correct(response, input_statement) if ANSWER_CONFIRMATION else False

            print('{0}: {1} ({2})'.format(bot_display_name, response, response.confidence))
        else:
            print('{0}: {1}'.format(bot_display_name, bot_bye_answer))

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
