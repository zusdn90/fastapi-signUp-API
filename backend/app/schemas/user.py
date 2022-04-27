from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

from pydantic import Field, validator
from pydantic.main import BaseModel

from app.core.utils.date_utils import D, KST


class LoginType(str, Enum):
    email: str = "email"
    phone_number: str = "mobile"


class Login(BaseModel):
    id: str = "01012341234 or test@gmail.com"
    password: str = "1234!!"

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: Optional[int] = Field(None, description="DB ID")
    name: Optional[str] = Field(None, description="이름")
    email: Optional[str] = Field(None, description="이메일")
    nick_name: Optional[str] = Field(None, description="닉네임")
    phone_number: Optional[str] = Field(None, description="전화번호")
    created_date: Optional[datetime] = Field(None, description="등록일")

    @validator("created_date")
    def parse_create_date(cls, value: Optional[datetime]):
        if value:
            return value.astimezone(KST)

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: Optional[str] = Field("홍길동", description="이름")
    email: Optional[str] = Field("honglidong@gmail.com", description="이메일")
    nick_name: Optional[str] = Field("홍당무", description="닉네임")
    phone_number: Optional[str] = Field("01012341234", description="전화번호")
    password: Optional[str] = Field("test!!", description="비밀번호")
    auth_number: str = "전화번호 인증 후 받은 번호 ex) 349503"

    class Config:
        orm_mode = True


class UserPhoneNumber(BaseModel):
    phone_number: Optional[str] = "01012341234"
