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

# Сохраняем название картинки
def save_picture_name(mdb, picture):
    photo = mdb.photography.find_one({'name': picture}) # Поиск картинки по названию файла
    if not photo: # Если такого нет, создаем словарь с данными
        photo = {'name': picture,
                'file_id': None,
                'like': 0,
                'dislike': 0,
                'user_id': []}
        mdb.photography.insert_one(photo) # Сохраняем словарь в коллекцию photography
    return photo

# Сохраняем file_id отправленной картинки
def save_file_id(mdb, picture, msg):
    mdb.photography.update_one(
        {'name': picture},
        {'$set': {'file_id': msg.photo[0].file_id}})

# Счетчик like и dislike
def save_like_dislike(mdb, query, data):
    file_id = query.message.photo[0].file_id # Получаем file_id
    photo = mdb.photography.find_one({'file_id': file_id}) # Поиск картинки по file_id
    if query.message.chat.id not in photo['user_id']:
        if data == 1:
            new_like = photo['like'] + data
            mdb.photography.update_one(
                {'file_id': file_id},
                {'$set': {'like': new_like}, '$addToSet': {'user_id': query.message.chat.id}})
        else:
            new_dislake = photo['dislake'] - data
            mdb.photography.update_one(
                {'file_id': file_id},
                {'$set': {'dislake': new_dislake}, '$addToSet': {'user_id': query.message.chat.id}})