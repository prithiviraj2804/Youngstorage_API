from fastapi import APIRouter
from ..database import db
from ..lib.wg.wireguard import addWireguard
from ..lib.docker.dockerGenrator import spawnContainer, IpRange65535


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome To YoungStorage API Service", "status": True}


@router.get("/deploy")
def Deploy():
    return spawnContainer("bhadri2002", "1")


@router.get("/addpeer")
def addPeer():
    return addWireguard("bhadri2002", "1", "172.20.0.2")


@router.get("/iplist/{ip}")
def iplist(ip):
    return IpRange65535(ip)
