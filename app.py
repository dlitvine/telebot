from utils import Currencies, CurrencyConverter, InputException
import telebot
from config import TM_TOKEN

bot = telebot.TeleBot(TM_TOKEN)


@bot.message_handler(commands=['start', ])
def send_start(message):
    bot.reply_to(message, f"Welcome {message.chat.first_name} {message.chat.last_name} (aka {message.chat.username})")
    send_help(message)


@bot.message_handler(commands=['test', ])
def send_test(message):
    bot.reply_to(message, "Test is successful, bot is listening")


@bot.message_handler(commands=['values', ])
def send_values(message):
    cur_text = "Example of currency codes:"
    for cur_key in Currencies.keys():
        cur_value = Currencies.get(cur_key)
        cur_str = f"{cur_key}: {cur_value}"
        cur_text = "\n".join((cur_text, cur_str))
    cur_text = "\n".join((cur_text, "For all supported currencies please refer to:"))
    cur_text = "\n".join((cur_text, "https://www.exchangerate-api.com/docs/supported-currencies"))
    bot.reply_to(message, cur_text)


@bot.message_handler(commands=['help', ])
def send_help(message):
    bot.reply_to(message, f"Here is help menu: \n"
                          f"To test bot enter /test \n"
                          f"To list supported currencies and find the codes enter /values\n"
                          f"To convert one currency into another, enter "
                          f"two currency codes and conversion amount separated by space\n"
                          f"Example: USD RUR 100\n"
                 )


@bot.message_handler(content_types='text')
def text_parser(message):
    inp_ = message.text.split()

    if len(inp_) != 3:
        raise InputException("Wrong number of parameters entered, please try again")
    try:
        float(inp_[2])
    except:
        raise InputException("Amount must be a number")

    target = inp_[0]
    quote = inp_[1]
    amount = inp_[2]

    result = CurrencyConverter.convert_currency(target, quote, amount)
    if result == "error" or result is None:
        bot.reply_to(message, f'Conversion unsuccessful, please try again later')
    else:
        str_ = f'Conversion result is: {amount} {target} is {result} {quote}'
        bot.reply_to(message, str_)


@bot.message_handler(content_types=['document', 'audio', 'photo', ])
def handle_docs_audio(message):
    bot.reply_to(message, 'I speak text only')


@bot.message_handler(content_types=['voice'])
def handle_docs_audio(message):
    bot.reply_to(message, "Your voice is beautiful, however I speak text only")


bot.polling(none_stop=True)
