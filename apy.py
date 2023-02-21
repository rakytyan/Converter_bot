import telebot
from config import keys, TOKEN
from utils import ConvertionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Этот простой и удобный бот для конвертации валют может:  \n- Показать список доступных для конвертации валют через команду /values \
    \n- Выполнить конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
- Помочь начать конвертацию /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    text = "Для расчета конвертации введите команду в следующем формате: \n <имя валюты> \
<в какую валюту перевести> \
<количество конвертируемой валюты> \n Показать список доступных для конвертации валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionExeption("Проверьте правильность команды конвертации валюты (введены три параметра через пробел).")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка пользователя. \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось произвести расчет для: \ n{e}")
    else:
        text = f"{amount} {quote} = {total_base} {base}"
        bot.send_message(message.chat.id, text)

bot.polling()


