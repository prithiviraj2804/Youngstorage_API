from fastapi import APIRouter, Depends
from ..database import db
from ..lib.models.userModels import Signup
from ..lib.auth.jwt import signJWT, decodeJWT
import re

router = APIRouter()


@router.post("/signup")
def signup(data: Signup):
    try:
        if db.user.find_one({"email": data.email}):
            return {"message": "email already exists", "status": False}
        elif db.user.find_one({"phone": data.phone}):
            return {"message": "phone number already exists", "status": False}
        else:
            _id = db.user.insert_one(data.dict()).inserted_id
            return {"message": "User Signed Up Successfully", "status": True, "Token": signJWT(_id)}
    except Exception as e:
        return {"message": str(e), "status": False}


@router.post("/admin")
def admin(_id=Depends(decodeJWT)):
    try:
        return {"message": "User Signed Up Successfully", "status": True, "id": _id}
    except Exception as e:
        return {"message": str(e), "status": False}
