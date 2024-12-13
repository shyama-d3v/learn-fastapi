from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()
try:
    DB_URL = os.getenv("DB_URL")
    # Connect to MongoDB
    client = MongoClient(
        DB_URL,
        server_api=ServerApi('1')
    )
    db = client.user_db
    collection_name = db["todo_collection"]

   
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"An error occurred while connecting to MongoDB: {e}")
