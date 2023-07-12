from fastapi import FastAPI
import uvicorn
from app.routers import root, userAuth, labs, network, services
from dotenv import load_dotenv
import os

os.umask(0o077)
load_dotenv()

app = FastAPI()
app.include_router(root.router)
app.include_router(userAuth.router)
app.include_router(labs.router)
app.include_router(network.router)
app.include_router(services.router)

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
