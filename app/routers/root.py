from fastapi import APIRouter
from ..database import db

router = APIRouter()

@router.get("/")
def root():
    return {"message":"Welcome To YoungStorage API Service","status":True}