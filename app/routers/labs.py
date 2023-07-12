from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends
from ..lib.docker.dockerGenerator import spawnContainer
from ..lib.auth.jwt import signJWT, Authenticator, UserRole
from ..database import db
from bson import ObjectId

router = APIRouter()


@router.get("/deploy")
def Deploy(data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        container = db.container.find_one({"_id": ObjectId(data["_id"])})
        if container:
            return {"message": "container data", "status": True, "data": container}
        else:
            return {"message": "container data", "status": True, "data": []}
    except Exception as e:
        return {"message": str(e), "status": False}

@router.post("/deploy")
def Deploy(background_task: BackgroundTasks, data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        container = db.container.find_one({"_id": ObjectId(data["_id"])})
        # if container already exist redeploy happens
        if container:
            return []
        else: # container not already exist new instance will be created
            return spawnContainer(data["_id"],data["username"], "1", background_task)
    except Exception as e:
        return {"message": str(e), "status": False}
