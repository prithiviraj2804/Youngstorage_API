from fastapi import APIRouter, Depends
from ..lib.wg.wireguard import addWireguard

router = APIRouter()

@router.get("/addpeer")
def addPeer():
    return addWireguard("bhadri2002", "1", "172.20.0.2")