from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

try:
    # Connect to MongoDB
    client = MongoClient(
        "mongodb+srv://shyama:shyama@cluster0.niex4.mongodb.net/",
        server_api=ServerApi('1')
    )
    db = client.user_db
    collection_name = db["todo_collection"]

   
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"An error occurred while connecting to MongoDB: {e}")
