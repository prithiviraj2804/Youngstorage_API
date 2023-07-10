from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from ...database import db
from bson import ObjectId
import os

# To get the secrets
# import secrets
# secrets.token_hex(32)


def signJWT(_id: str) -> str:
    payload = {
        "_id": _id,
        "exp": datetime.utcnow() + timedelta(minutes=int(os.getenv("JWT_EXPIRATION_TIME_IN_MIN")))
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"),
                       algorithm=os.getenv("JWT_ALGORITHM"))
    return token

def decodeJWT(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) ->str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        _id = payload.get("_id")
        
        if not _id:
            raise HTTPException(status_code=401, detail="Invalid token")
        else:
            if db.user.find_one({"_id":ObjectId(_id)}):
                return _id
            else:
                raise HTTPException(status_code=401, detail="Invalid token")        
    except jwt.exceptions.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

