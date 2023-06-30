from fastapi import APIRouter
from pydantic import BaseModel,EmailStr,Field,validator
from ..database import db

router = APIRouter()

password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"
phone_regex = "^[0-9]{10}$"

class Signup(BaseModel):
    email : EmailStr = Field(...,)
    password : str = Field(..., regex=password_regex)
    phone : str = Field(..., regex=phone_regex)

    @validator("email")
    def email_validation(cls,email):
        verify = email.split("@",-1)
        allowed = ["gmail.com",'hotmail.com',"outlook.com","icloud.com","protonmail.com","live.com"]
        if verify[1] not in allowed:
            raise {"message":"Please Enter Valid Email Domain","status":False}
        return email,verify
        
@router.post("/signup")
def signup(data:Signup):
    try:
        if db.user.find_one({"email":data.email}) or db.user.find_one({"phone":data.phone}):
            return {"message":"email or phone number already exists","status":False}
        else:
            db.user.insert_many(data.dict())
            return {"message":"User Signed Up Successfully","status":True}
    except Exception as e:
        return {"message":str(e),"status":False}