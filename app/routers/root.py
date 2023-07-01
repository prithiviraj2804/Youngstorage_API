import asyncio
from fastapi import APIRouter, Depends
from ..database import db,mqtt_client
from ..lib.wg.wireguard import addWireguard
from ..lib.docker.dockerGenrator import spawnContainer, IpRange65535

router = APIRouter()


@router.get("/")
async def root():
    for i in range(100):
        mqtt_client.publish("/topic/sample", f"container {i}")
    return {"message": "Welcome to the youngstorage API server", "status": True}


@router.get("/deploy")
def Deploy():
    return spawnContainer("bhadri2002", "1")


@router.get("/addpeer")
def addPeer():
    return addWireguard("bhadri2002", "1", "172.20.0.2")


@router.get("/iplist/{ip}")
def iplist(ip):
    return IpRange65535(ip)
