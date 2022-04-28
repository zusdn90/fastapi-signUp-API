from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import Field, validator
from pydantic.main import BaseModel

from app.core.utils.date_utils import D, KST


class LoginType(str, Enum):
    email: str = "email"
    phone_number: str = "mobile"


class Login(BaseModel):
    id: str
    password: str

    class Config:
        schema_extra = {
            "examples": {
                "email": {
                    "summary": "email 로그인",
                    "value": {
                        "id": "hongildong@gmail.com",
                        "password": "test!!!",
                    },
                },
                "mobile": {
                    "summary": "전화번호 로그인",
                    "value": {
                        "id": "01012341234",
                        "password": "test!!!",
                    },
                },
            }
        }


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
    name: str = Field(..., description="이름")
    email: str = Field(..., description="이메일")
    nick_name: Optional[str] = Field(..., description="닉네임")
    phone_number: str = Field(..., description="전화번호")
    password: str = Field(..., description="비밀번호")
    auth_number: str

    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                "email": {
                    "summary": "회원가입 입력 예시",
                    "value": {
                        "name": "홍길동",
                        "email": "hongildong@gmail.com",
                        "nick_name": "당근",
                        "phone_number": "01012341234",
                        "password": "test!!",
                        "auth_number": "394721",
                    },
                }
            }
        }


class UserPhoneNumber(BaseModel):
    phone_number: str

    class Config:
        schema_extra = {
            "examples": {
                "phone_number": {
                    "summary": "전화번호 입력 예시",
                    "value": {
                        "phone_number": "01012341234",
                    },
                }
            }
        }
