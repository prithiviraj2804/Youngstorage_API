from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo = "mongodb://root:example@localhost:27017/"

config = Settings()