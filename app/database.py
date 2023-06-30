from pymongo import MongoClient
from app.config import config

client = MongoClient(config.mongo)

db = client["youngstorage"]
