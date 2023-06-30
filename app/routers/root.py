from fastapi import APIRouter
from ..database import db

router = APIRouter()

@router.get("/")
def root():
    query = db.user.insert_one({"name":"test","status":True}).inserted_id
    return {"message":"Welcome To YoungStorage API Service","status":True}