from datetime import datetime
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel

#######################################
# User Parameter schema
#######################################
class TokenCreate(BaseModel):
    phone_number: str = "01012341234"
    password: str = "1234!!"


class Token(BaseModel):
    Authorization: str = None


class UserMe(BaseModel):
    id: int
    user_id: str = None
    email: str = None
    name: str = None
    phone_number: str = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str = "홍길동"
    phone_number: str = "01012341234"
    email: str = "hongildong@gmail.com"
    password: str = "1234!!"
    nick_name: str = "홍당무"
    auth_number: str = "349503"

    class Config:
        orm_mode = True


class UserFindPwd(BaseModel):
    auth_number: str = "349503"
    password: str = "1234!!"


class UserPhoneNumberAuth(BaseModel):
    phone_number: Optional[str] = "01012341234"


class AuthNumber(BaseModel):
    auth_number: str = "349503"
