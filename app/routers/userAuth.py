from fastapi import APIRouter, Depends, Response
from ..database import db
from ..lib.models.userModels import Signup, Signin
from ..lib.auth.jwt import signJWT, Authenticator, UserRole
from ..lib.auth.email_sender import send_email_async
from bson import ObjectId

router = APIRouter()


@router.post("/signup")
async def signup(data: Signup):
    try:
        if db.user.find_one({"email": data.email}):
            return {"message": "email already exists", "status": False}
        elif db.user.find_one({"phone": data.phone}):
            return {"message": "phone number already exists", "status": False}
        else:
            _id = db.user.insert_one(data.create_user()).inserted_id
            await send_email_async("User verification", data.email, signJWT(str(_id), 15))
            return {"message": "User Signed Up Successfully. Now check the email", "status": True}
    except Exception as e:
        return {"message": str(e), "status": False}


@router.get("/userverify")
def user_verify(_id=Depends(Authenticator(False, UserRole.user).signupJWT)):
    print("say somthing:", _id)
    if db.user.update_one({"_id": ObjectId(_id)}, {"$set": {"user_verified": True}}):
        return {"message": "User Verified Successfully", "status": True}
    else:
        return {"message": "User Not Verified", "status": False}


@router.post("/signin")
async def signup(response: Response, data: Signin):
    try:
        user = db.user.find_one({"email": data.email})
        data = data.verify_user(user["password"])
        if "_id" in user and data:
            if user["user_verified"] == True:
                response.headers["Authorization"] = f"Bearer {signJWT(str(user['_id']),user_verified=True)}"
                return {"message": "User Signin Successfull", "status": True}
            else:
                return {"message": "User Not Verified", "status": False}
        else:
            return {"message": "Invalid Credentials", "status": False}
    except Exception as e:
        return {"message": str(e), "status": False}


@router.get("/user")
def user(data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    return {"message": data, "status": True}
