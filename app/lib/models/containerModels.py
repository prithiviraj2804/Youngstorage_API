class ContainerModels:
    def __init__(self, **kwargs) -> None:
        self.userId = kwargs["userId"]

    def AddNewContainer(self):
        return {
            "userId": self.userId,
            "ipAddress": self.ipaddress,
            "username": self.username,
            "password": self.password,
            "vscode": self.vscode,
            "vsPassword": self.vsPassword
        }


class NetworkModel:
    def __init__(self, userId,
                 ipaddress,
                 username,
                 password,
                 vscode,
                 vsPassword) -> None:
        self.userId = userId,
        self.ipaddress = ipaddress,
        self.username = username,
        self.password = password,
        self.vscode = vscode,
        self.vsPassword = vsPassword
