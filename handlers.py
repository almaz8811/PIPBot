from utility import get_keyboard, SMILE
from bs4 import BeautifulSoup
from glob import glob # Получить список названий картинок
from random import choice # Получить случайный элемент из списка
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler
import requests
from emoji import emojize
from mongodb import search_or_save_user, mdb, save_user_anketa


# Функция sms будет вызванна при отправке пользователем /start
# Внутри функции будет описанна логика при ее вызове
def sms(bot, update):
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    print(user)
    smile = emojize(choice(SMILE), use_aliases = True)
    print('Кто-то отправил команду /start, что мне делать???') # Вывод сообщения в консоль
    bot.message.reply_text('Здравствуйте, {}! \nПоговорите со мной {}'.format(bot.message.chat.first_name, smile), reply_markup = get_keyboard())

# Функция отправляет случайную картинку
def send_meme(bot, update):
    lists = glob('images/*') # Создаем список из названий картинок
    picture = choice(lists) # Берем из списка одну картинку
    update.bot.send_photo(chat_id = bot.message.chat_id, photo = open(picture, 'rb')) # Отправляем картинку

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

# Функция печатает и отвечает на полученный контакт
def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text('{}, мы получили ваш номер телефона'.format(bot.message.chat.first_name))

# Функция печатает и отвечает на полученные геоданные
def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили вае местоположение'.format(bot.message.chat.first_name))

def anketa_start(bot, update):
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    if 'anketa' in user:
        text = '''Ваш предыдущий результат:
        <b>Имя:</b> {name}
        <b>Возраст:</b> {age}
        <b>Оценка:</b> {evaluation}
        <b>Комментарий:</b> {comment}
        Данные будут обновлены!
        Как вас зовут?
        '''.format(**user['anketa'])
        bot.message.reply_text(text, parse_mode = ParseMode.HTML, reply_markup = ReplyKeyboardRemove())
        return 'user_name'
    else:
        bot.message.reply_text('Как вас зовут?', reply_markup = ReplyKeyboardRemove())  # вопрос и убираем основную клавиатуру
        return 'user_name'  # ключ для определения следующего шага


def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text  # временно сохраняем ответ
    bot.message.reply_text('Сколько вам лет?')  # задаем вопрос
    return 'user_age'  # ключ для определения следующего шага


def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [['1', '2', '3', '4', '5']]  # создаем клавиатуру
    bot.message.reply_text(
        'Оцените статью от 1 до 5',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard = True, one_time_keyboard = True))  # при нажатии клавиатура исчезает
    return 'evaluation'  # ключ для определения следующего шага


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [['Пропустить']]  # создаем клавиатуру
    bot.message.reply_text('Напишите отзыв или нажмите кнопку пропустить этот шаг.',
                                reply_markup = ReplyKeyboardMarkup(
                                reply_keyboard, resize_keyboard = True, one_time_keyboard = True))  # клава исчезает
    return 'comment'  # ключ для определения следующего шага


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # временно сохраняем ответ
    user = search_or_save_user(mdb, bot.effective_user, bot.message) # Получаем данные из базы данных
    anketa = save_user_anketa(mdb, user, update.user_data) # Передаем и получаем результаты анкеты
    print(anketa)
    text = '''Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий:</b> {comment}
    '''.format(**update.user_data)
    bot.message.reply_text(text, parse_mode = ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text('Спасибо вам за комментарий!', reply_markup = get_keyboard())  # сообщение и возвр. осн. клаву
    return ConversationHandler.END  # выходим из диалога


def anketa_exit_comment(bot, update):
    update.user_data['comment'] = None
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    save_user_anketa(mdb, user, update.user_data)
    text = '''Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}'''.format(**update.user_data)
    bot.message.reply_text(text, parse_mode = ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text('Спасибо!', reply_markup = get_keyboard())  # отправляем сообщение и возвращаем осн. клаву
    return ConversationHandler.END  # выходим из диалога


def dontknow(bot, update):
    bot.message.reply_text('Я вас не понимаю, выберите оценку на клавиатуре!')