from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..lib.wg.wireguard import addWireguard
from ..lib.auth.jwt import Authenticator, UserRole
from ..lib.docker.dockerGenerator import IpRange65535
from ..database import db
from ..lib.models.networkModels import DomainNetwork
router = APIRouter()


class Devices(BaseModel):
    Name: str


class Domain(BaseModel):
    Name: str

# this is for to get the entire network list


@router.get("/networks")
def getUserPeer(data: dict = Depends(Authenticator(True, UserRole.user).signupJWT)):
    network = db.network.find_one({"userId": str(data["_id"])})
    return {"message": "list of network", "status": True, "data": network}


# this function is to add new peer for the user
@router.post("/addpeer")
def addUserPeer(devicename: Devices, data: dict = Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        baselist = list(db.baselist.find())
        if len(baselist) == 1:
            ip = baselist[0]["ip"]
            ipdata = IpRange65535(ip)
            if ipdata["status"]:
                ip = ipdata["message"]
                network = db.network.find_one({"userId": str(data["_id"])})
                status = {}
                if network:
                    status = addWireguard(data["_id"], data["username"],
                                          str(network["currentPeer"]+1), ip, deviceName=str(devicename.Name), client=True)
                else:
                    status = addWireguard(data["_id"], data["username"],
                                          "1", ip, deviceName=str(devicename.Name), client=True)

                if status["status"]:
                    db.baselist.update_one({"_id": baselist[0]["_id"]}, {
                        "$set": {"ip": ip, "ipissued": baselist[0]["ipissued"]+1}})
                    return status
        else:
            raise ValueError("Please check the baselist")
    except ValueError as e:
        return {"message": str(e), "status": False}
    except Exception as e:
        # Return error response with a status code of 500
        return {"message": str(e), "status": False}


# this function is to add new domain
@router.post("/addomain")
def addUserPeer(domainname: Domain, data: dict = Depends(Authenticator(True, UserRole.user).signupJWT)):
    try:
        domain = DomainNetwork(str(data["_id"]), domainname.Name).addDomain()
        return {"message": f"{domain} {domainname.Name} added successfully", "status": True}
    except ValueError as e:
        return {"message": str(e), "status": False}
    except Exception as e:
        return {"message": str(e), "status": False}
