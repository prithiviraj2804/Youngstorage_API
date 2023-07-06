import asyncio
from fastapi import APIRouter, Depends
from ..database import db,mqtt_client
from ..lib.wg.wireguard import addWireguard
from ..lib.docker.dockerGenerator import spawnContainer
from fastapi import BackgroundTasks

router = APIRouter()


@router.get("/")
async def root():
    for i in range(100):
        mqtt_client.publish("/topic/sample", f"container {i}")
    return {"message": "Welcome to the youngstorage API server", "status": True}


@router.get("/deploy")
def Deploy(background_task:BackgroundTasks):
    return spawnContainer("bhadri2002", "1",background_task)


@router.get("/addpeer")
def addPeer():
    return addWireguard("bhadri2002", "1", "172.20.0.2")