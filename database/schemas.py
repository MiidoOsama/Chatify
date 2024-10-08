# database/schemas.py
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ServerSchema(BaseModel):
    name: str
    status: str
    code: str
    type: str
