from datetime import datetime
from typing import List

from pydantic import Field
from pydantic.main import BaseModel


class UserCreate(BaseModel):
    phone_number: str = None
    password: str = None


class Token(BaseModel):
    Authorization: str = None


class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: int
    user_id: str = None
    email: str = None
    name: str = None
    phone_number: str = None

    class Config:
        orm_mode = True