from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from ...database import db
from bson import ObjectId
from enum import Enum
import os

# To get the secrets
# import secrets
# secrets.token_hex(32)


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"


def signJWT(_id: str, exp: int = 60*24, user_verified: bool = False, role: UserRole = UserRole.user) -> str:
    payload = {
        "_id": _id,
        "user_verified": user_verified,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=exp)
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"),
                       algorithm=os.getenv("JWT_ALGORITHM"))
    return token


class Authenticator:
    def __init__(self, user_verified: bool, role: UserRole):
        self.user_verified = user_verified
        self.role = role

    def signupJWT(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
        try:
            token = credentials.credentials
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms=[os.getenv("JWT_ALGORITHM")]
            )
            _id = payload.get("_id")
            role = payload.get("role")
            user_verified = payload.get("user_verified")
            exp = payload.get("exp")

            if not _id or not exp or not role or not str(user_verified):
                raise HTTPException(status_code=401, detail="Invalid token")

            if self.user_verified:
                if self.user_verified == user_verified and self.role == role:
                    data = db.user.find_one({"_id": ObjectId(_id), "role": role, "user_verified": user_verified})
                    if data:
                        data["_id"] = str(data["_id"])
                        data.pop("password")
                        return data
                    else:
                        raise HTTPException(
                            status_code=401, detail="Invalid token")
                else:
                    raise HTTPException(
                        status_code=401, detail="Invalid token")
            else:
                if db.user.find_one({"_id": ObjectId(_id), "role": role, "user_verified": user_verified}):
                    return _id
                else:
                    raise HTTPException(
                        status_code=401, detail="Invalid token")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")
