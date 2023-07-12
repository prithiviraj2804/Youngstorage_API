from ...database import db


class NetworkModel:
    def __init__(self, userId: str) -> None:
        self.db = db
        self.userId = userId
        self.getNetwork()

    def getNetwork(self):
        user = self.db.network.find_one({"userId": self.userId})
        if user:
            self.labPeer = user["labPeer"]
            self.peerList = user["peerList"]
            self.domainList = user["domainList"]
            self.currentPeer = user["currentPeer"]
            self.maxPeer = user["maxPeer"]
            self.currentDomain = user["currentDomain"]
            self.maxDomain = user["maxDomain"]
            self.haveNetwork = True
        else:
            self.labPeer = {}
            self.peerList = []
            self.domainList = []
            self.currentPeer = 0
            self.maxPeer = 3
            self.currentDomain = 0
            self.maxDomain = 5
            self.haveNetwork = False


class WireguardNetwork(NetworkModel):
    def __init__(self, userId: str, ipaddress: str, publickey: str, devicename: str) -> None:
        super().__init__(userId)
        self.ipAddress = ipaddress
        self.publicKey = publickey
        self.deviceName = devicename

    def addLabPeer(self):
        self.labPeer = {
            "ipAddress": self.ipAddress,
            "publicKey": self.publicKey,
            "deviceName": self.deviceName
        }
        document = {
                'userId': self.userId,
                'labPeer':self.labPeer,
                'peerList': self.peerList,
                'domainList': self.domainList,
                'currentPeer': self.currentPeer,
                'maxPeer': self.maxPeer,
                'currentDomain': self.currentDomain,
                'maxDomain': self.maxDomain
            }
        if self.haveNetwork:
            self.db.network.update_one({"userId": self.userId}, {"$set": {"labPeer": self.labPeer}})
        else:
            self.db.network.insert_one(document)

    def addPeer(self):
        # Example: Save network model data to the database
        if (self.currentPeer < self.maxPeer):
            self.peerList.append({
                "ipAddress": self.ipAddress,
                "publicKey": self.publicKey,
                "deviceName": self.deviceName
            })
            self.currentPeer += 1

            document = {
                'userId': self.userId,
                'labPeer':self.labPeer,
                'peerList': self.peerList,
                'domainList': self.domainList,
                'currentPeer': self.currentPeer,
                'maxPeer': self.maxPeer,
                'currentDomain': self.currentDomain,
                'maxDomain': self.maxDomain
            }
            if self.haveNetwork:
                self.db.network.update_one({"userId": self.userId}, {
                                           "$set": {"peerList": self.peerList, "currentPeer": self.currentPeer}})
            else:
                self.db.network.insert_one(document)
        else:
            raise ValueError("max peer reached")


class DomainNetwork(NetworkModel):
    def __init__(self, userId: str, domainName: str) -> None:
        super().__init__(userId)
        self.domainName = domainName

    def addDomain(self):
        # Example: Save network model data to the database
        if (self.currentDomain < self.maxDomain):
            self.domainList.append({
                "domainName": self.domainName,
            })
            self.currentDomain += 1

            document = {
                'userId': self.userId,
                'labPeer':self.labPeer,
                'peerList': self.peerList,
                'domainList': self.domainList,
                'currentPeer': self.currentPeer,
                'maxPeer': self.maxPeer,
                'currentDomain': self.currentDomain,
                'maxDomain': self.maxDomain
            }
            if self.haveNetwork:
                self.db.network.update_one({"userId": self.userId}, {
                                           "$set": {"domainList": self.domainList, "currentDomain": self.currentDomain}})
            else:
                self.db.network.insert_one(document)
        else:
            raise ValueError("max domain reached")
