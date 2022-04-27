from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class Token(BaseModel):
    Authorization: str = None


class UserToken(BaseModel):
    name: Optional[str] = Field(None, description="이름")
    email: Optional[str] = Field(None, description="이메일")
    nick_name: Optional[str] = Field(None, description="닉네임")
    phone_number: Optional[str] = Field(None, description="전화번호")

    class Config:
        orm_mode = True


class UserFindPwd(BaseModel):
    phone_number: str = "01012341234"
    auth_number: str = "349503"
    password: str = "1234!!"


class AuthNumber(BaseModel):
    auth_number: str = "349503"
