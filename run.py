from fastapi import FastAPI
import uvicorn
from app.routers import root,signup

app = FastAPI()
app.include_router(root.router)
app.include_router(signup.router)

if __name__ == "__main__":
    uvicorn.run("run:app",host="0.0.0.0",port=8000,reload=True)