from pydantic import BaseSettings
from pymongo import MongoClient

class Settings(BaseSettings):
    mongo = "mongodb://youngstorage:dotmail123@mongodb.youngstorage.in:27017/?authMechanism=DEFAULT&authSource=youngstorage"

config = Settings()