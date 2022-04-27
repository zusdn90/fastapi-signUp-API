from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

from pydantic import Field
from pydantic.main import BaseModel


class Token(BaseModel):
    Authorization: str = None


class UserToken(BaseModel):
    token: str = None


class UserFindPwd(BaseModel):
    phone_number: str = "01012341234"
    auth_number: str = "349503"
    password: str = "1234!!"


class AuthNumber(BaseModel):
    auth_number: str = "349503"
