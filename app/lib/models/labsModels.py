from ...database import db


class ContainerModels:
    def __init__(self, userId: str) -> None:
        self.db = db
        self.userId = userId

    def addLab(self, ipaddress: str, username: str, password: str):
        try:
            document = {
                "userId": self.userId,
                "ipAddress": ipaddress,
                "username": username,
                "password": password,
                "vsCode": None,
                "vsPassword": None
            }
            self.db.labs.insert_one(document)
        except Exception as e:
            raise (e)

    def upgradeVScode(self, vscode: str, vsPassword: str):
        try:
            self.db.labs.update_one({"userId": self.userId}, {
                "$set": {"vsCode": vscode, "vsPassword": vsPassword}})
        except Exception as e:
            raise (e)
