# database/schemas.py
from pydantic import BaseModel

class ServerSchema(BaseModel):
    name: str
    status: str
    code: str
    type: str
