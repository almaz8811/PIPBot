from pymongo import MongoClient

client = MongoClient('mongodb+srv://almaz8811:almaz084284@pipbot-s1ibg.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = client.test
db.chats.insert_one({'user': 'Александр', 'phone': '+79383575333'})