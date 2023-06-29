from fastapi import APIRouter
from pydantic import BaseModel,EmailStr,Field,validator
from ..database import db

router = APIRouter()

password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"

class Signup(BaseModel):
    email : EmailStr
    password : str = Field(..., regex=password_regex)
    phone : int

    # @validator("email")
    # def email_validation(cls,email):
    #     verify = email.split("@",-1)
    #     allowed = ["gmail.com",'hotmail.com',"outlook.com","icloud.com"]
    #     if verify[1] not in allowed:
    #         return {"message":"Please Enter Valid Email Domain","status":False}
        

@router.post("/signup")
async def signup(data : Signup):
    try:
        if data:
            return {"message":data,"status":True}
        
    except Exception as e:
        return {"message":str(e),"status":False}