from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends
from ..lib.docker.dockerGenerator import spawnContainer
from ..lib.auth.jwt import signJWT, Authenticator, UserRole

router = APIRouter()

@router.get("/deploy")
def Deploy(background_task: BackgroundTasks,data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    return spawnContainer("bhadri2002", "1", background_task)