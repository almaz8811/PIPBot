from telegram import ReplyKeyboardMarkup, KeyboardButton # Импорт клавиатуры

SMILE = ['😊', '😀', '😇', '🤠', '😎', '🤓', '👶', '🧑‍🚀', '👮', '🦸', '🧟']
CALLBACK_BUTTON_PICTURE = 'Картинка 🏞'
CALLBACK_BUTTON_PEN = 'Заполнить анкету 🖌'
CALLBACK_BUTTON_START = 'Начать 🎰'
CALLBACK_BUTTON_JOKE = 'Анекдот 🎭'

# Функция создает клавиатуру и ее разметку
def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([[CALLBACK_BUTTON_START, CALLBACK_BUTTON_JOKE],
                                        [contact_button, location_button],
                                        [CALLBACK_BUTTON_PEN, CALLBACK_BUTTON_PICTURE]
                                        ], resize_keyboard = True)  # добавляем кнопки
    return my_keyboard