import asyncio
from fastapi import APIRouter, Depends
from ..database import db,mqtt_client
from ..lib.wg.wireguard import addWireguard
from ..lib.docker.dockerGenerator import spawnContainer
from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
from ..lib.banner import Banner
router = APIRouter()


@router.get("/")
async def root():
    # for i in range(100):
    #     mqtt_client.publish("/topic/sample", f"container {i}")
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body >
           
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/deploy")
def Deploy(background_task:BackgroundTasks):
    return spawnContainer("bhadri2002", "1",background_task)


@router.get("/addpeer")
def addPeer():
    return addWireguard("bhadri2002", "1", "172.20.0.2")