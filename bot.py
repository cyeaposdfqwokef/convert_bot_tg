import json
import telebot
from extensions import CurrencyConverter, APIException

# Чтение токена бота из конфига
with open('config.py', 'r') as f:
    config = json.load(f)
    bot_token = config['bot_token']

# Создание экземпляра бота
bot = telebot.TeleBot(bot_token)

# Обработчик команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Привет! Я бот для конвертации валют. Чтобы узнать цену валюты, отправь мне сообщение в формате:\n<имя валюты, цену которой ты хочешь узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\nНапример: USD RUB 100\n\nДоступные команды:\n/values - список доступных валют"
    bot.reply_to(message, instructions)

# Обработчик команды /values
@bot.message_handler(commands=['values'])
def send_currency_list(message):
    currencies = "Доступные валюты:\n- USD (Доллар США)\n- EUR (Евро)\n- RUB (Российский рубль)"
    bot.reply_to(message, currencies)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    text = message.text.upper().split()
    if len(text) != 3:
        error_message = "Неверный формат сообщения. Пожалуйста, используйте формат: <имя валюты, цену которой ты хочешь узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>"
        bot.reply_to(message, error_message)
    else:
        base_currency = text[0]
        quote_currency = text[1]
        amount = float(text[2])
        try:
            converted_amount = CurrencyConverter.get_price(base_currency, quote_currency, amount)
            result_message = f"{amount} {base_currency} = {converted_amount} {quote_currency}"
            bot.reply_to(message, result_message)
        except APIException as e:
            error_message = f"Ошибка: {e.message}"
            bot.reply_to(message, error_message)

# Запуск бота
bot.polling()