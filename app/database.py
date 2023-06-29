from pymongo import MongoClient
from app.config import config

sync_client = MongoClient(config.mongo)

db = sync_client["youngstorage"]
