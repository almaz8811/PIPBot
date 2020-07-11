from pymongo import MongoClient
import os
# from settings import MONGO_DB, MONGODB_LINK

mdb = MongoClient(os.environ['MONGODB_LINK'])[os.environ['MONGO_DB']] # Переменная для работы с базой данных

def search_or_save_user(mdb, effective_user, message):
    user = mdb.users.find_one({'user_id': effective_user.id}) # Поиск в коллекции users по user.id
    if not user: # Если такого нет, то создаем словарь с данными
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'chat_id': message.chat.id
        }
        mdb.users.insert_one(user) # Сохраняем в коллекцию users
    return user

# Сохраняем - обновляем результаты анкеты и возвращаем результат
def save_user_anketa(mdb, user, user_data):
    mdb.users.update_one(
        {'_id': user['_id']}, # Поиск данных юзера по id
        {'$set': {'anketa': {'name': user_data['name'], # Обновляем данные, сохраняем результаты анкетирования
                            'age': user_data['age'],
                            'evaluation': user_data['evaluation'],
                            'comment': user_data['comment']
                            }
                }
        }
    )
    return user