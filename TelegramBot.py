
import telebot
from Extensions import *
from Configuration import *
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Привет!\n" \
           "Я - бот-конвертер валют\n" \
           "Узнать доступные валюты напиши /value\n" \
           "Если нужна помощь напиши /help"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Чтобы узнать курс валюты надо:\n " \
           "ввести название интересующей валюты\n" \
           "название валюты, в которую перевести\n" \
           "и сумму для конвертации\n" \
           "вводить через пробел"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['value'])
def values(message: telebot.types.Message):
    text = """Доступные валюты:\n 
           доллар USD\n 
           евро EUR\n
           рубль RUB"""
    bot.reply_to(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Вы забыли что-то указать')

        reply = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, reply)

@bot.message_handler(content_types=['text', ])
def changer(message: telebot.types.Message):
    base, sym, amount = message.text.split('')
    r = requests.get(f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={base_key}&tsyms={sym_key}")
    resp = json.loads(r.content)[base]
    total_sum = resp[sym_key] * float(amount)
    text = f"{amount} {base} в {sym} - {total_sum}"
    bot.reply_to(message.chat.id, text)


bot.polling()
