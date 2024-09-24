# database/models.py
class ServerModel:
    def __init__(self, name: str, status: str, code: str, type: str):
        self.name = name
        self.status = status
        self.code = code
        self.type = type
    
    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "code": self.code,
            "type": self.type
        }
