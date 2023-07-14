from fastapi import BackgroundTasks, status, Response, APIRouter, Depends
from ..lib.docker.dockerGenerator import spawnContainer, reDeploy
from ..lib.auth.jwt import signJWT, Authenticator, UserRole
from ..database import db, mqtt_client
import subprocess

router = APIRouter()

# get the container status and details


@router.get("/deploy")
def getContainerData(data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        container = db.labs.find_one({"userId": data["_id"]})
        if container:
            container["_id"] = str(container["_id"])
            return {"message": "container data", "status": True, "data": container}
        else:
            return {"message": "container data", "status": True, "data": []}
    except Exception as e:
        return {"message": str(e), "status": False}


# post to deploy new Instance or redeploy the existing Instance
@router.post("/deploy")
def createContainer(background_task: BackgroundTasks, data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        # print(WireguardNetwork(userId=data["_id"],devicename="phone",ipaddress="172.0.0.2",publickey="123123").addPeer())
        container = db.labs.find_one({"userId": data["_id"]})
        # if container already exist redeploy happens
        if container:
            return reDeploy(data["_id"], data["username"], "lab", background_task)
        else:  # container not already exist new instance will be created
            return spawnContainer(data["_id"], data["username"], "lab", background_task)
    except ValueError as e:
        return {"message": str(e), "status": False}
    except Exception as e:
        return {"message": str(e), "status": False}


@router.post("/upvscode")
def upVScode(data=Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        # instance name
        username = data["username"]

        # command to up vscode in web
        command = f'docker exec -it {username} bash -c "source code-server.sh"'

        # Execute the command using subprocess
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()

        for i in str(stdout.decode()).strip().split("\r\n"):
            mqtt_client.publish("/topic/sample", i)

        # Check the command execution status
        if process.returncode == 0:
            # Print the command output
            return {"message": "Command executed successfully", "status": True}
        else:
            return {"message": f'Command failed with exit code: {process.returncode}', "status": False}

    except Exception as e:
        return {"message": str(e), "status": False}
