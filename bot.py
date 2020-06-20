from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from telegram import ReplyKeyboardMarkup # Импорт клавиатуры
from bs4 import BeautifulSoup
import requests

# Функция sms будет вызванна при отправке пользователем /start
# Внутри функции будет описанна логика при ее вызове
def sms(bot, update):
    print('Кто-то отправил команду /start, что мне делать???') # Вывод сообщения в консоль
    bot.message.reply_text('Здравствуйте, {}! \nПоговорите со мной.'.format(bot.message.chat.first_name), reply_markup = get_keyboard())

def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random') # Отправляем запрос к странице
    page = BeautifulSoup(receive.text, 'html.parser') # Подключаем html парсер, получаем текст страницы
    find = page.select('.anekdot_text') # Из страницы html получаем class = '.anekdot_text'
    for text in find:
        page = (text.getText().strip()) # Из class = '.anekdot_text' получаем текст и убираем пробелы по сторонам
    bot.message.reply_text(page) # Отправляем один анекдот, последний

# Функция parrot() отвечает тем же сообщением, которое пользователь отправил
def parrot(bot, update):
    print(bot.message.text) # Печатаем сообщение на экране
    bot.message.reply_text(bot.message.text) # Отправляем обратно сообщение, которое пользователь написал

# Функция создает клавиатуру и ее разметку
def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'], ['Начать']], resize_keyboard = True) # Добавляем кнопку
    return get_keyboard

# Создаем функцию main(), которая соединяется с сервисом Telegram
def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context = True)
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()

main()