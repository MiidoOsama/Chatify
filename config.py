
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://chatify:chatify@chatify.dzioy.mongodb.net/?retryWrites=true&w=majority&appName=Chatify"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.chatify_db
collection = db["servers"]