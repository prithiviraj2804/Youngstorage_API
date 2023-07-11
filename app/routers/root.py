import asyncio
from fastapi import APIRouter, Depends
from ..database import db, mqtt_client
from ..lib.wg.wireguard import addWireguard
from ..lib.docker.dockerGenerator import spawnContainer
from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
from ..lib.banner import Banner

router = APIRouter()


@router.get("/")
def root():
    return {"message": "welcome to the Youngstorage API server", "status": True}


@router.get("/deploy")
def Deploy(background_task: BackgroundTasks):
    return spawnContainer("bhadri2002", "1", background_task)


@router.get("/addpeer")
def addPeer():
    return addWireguard("bhadri2002", "1", "172.20.0.2")
