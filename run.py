from fastapi import FastAPI
import uvicorn
from app.routers import root,userAuth
from dotenv import load_dotenv
import os

os.umask(0o077)
load_dotenv()

app = FastAPI()
app.include_router(root.router)
app.include_router(userAuth.router)

if __name__ == "__main__":
    uvicorn.run("run:app",host="0.0.0.0",port=8000,reload=True)