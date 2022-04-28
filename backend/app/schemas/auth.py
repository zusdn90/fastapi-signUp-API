from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class Token(BaseModel):
    Authorization: str = None


class UserToken(BaseModel):
    name: str = Field(..., description="이름")
    email: str = Field(..., description="이메일")
    nick_name: Optional[str] = Field(None, description="닉네임")
    phone_number: str = Field(..., description="전화번호")

    class Config:
        orm_mode = True


class UserFindPwd(BaseModel):
    phone_number: str
    auth_number: str
    password: str

    class Config:
        schema_extra = {
            "examples": {
                "phone_number": {
                    "summary": "비밀번호 재설정 입력 예시",
                    "value": {
                        "phone_number": "01012341234",
                        "auth_number": "343832",
                        "password": "newpassword!!",
                    },
                }
            }
        }


class AuthNumber(BaseModel):
    auth_number: str = "349503"
