from pymongo import MongoClient
from settings import MONGO_DB, MONGODB_LINK

mdb = MongoClient(MONGODB_LINK)[MONGO_DB] # Переменная для работы с базой данных

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