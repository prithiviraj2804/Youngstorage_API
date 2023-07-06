from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel, EmailStr, Field, validator
from ..database import db
import re

router = APIRouter()

password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,64}$"
phone_regex = r"^[0-9]{10}$"


class Signup(BaseModel):
    email: EmailStr
    password: str
    phone: str
    

    @validator("email")
    def email_validation(cls, email):
        verify = email.split("@")
        allowed = ["gmail.com", 'hotmail.com', "outlook.com",
                   "icloud.com", "protonmail.com", "live.com"]
        if verify[1] not in allowed:
            raise ValueError("Please Enter Valid Email Domain")
        return email

    @validator("password")
    def password_validation(cls, password):
        if not re.match(password_regex, password):
            raise ValueError(
                "Please enter a password that meets the required pattern")
        return password

    @validator("phone")
    def phone_validation(cls, phone):
        if not re.match(phone_regex, phone):
            raise ValueError("Please enter a valid phone number")
        return phone


@router.post("/signup")
def signup(data: Signup):
    try:
        if db.user.find_one({"email": data.email}):
            return {"message": "email already exists", "status": False}
        elif db.user.find_one({"phone": data.phone}):
            return {"message": "phone number already exists", "status": False}
        else:
            db.user.insert_one(data.dict())
            return {"message": "User Signed Up Successfully", "status": True}
    except Exception as e:
        return {"message": str(e), "status": False}
