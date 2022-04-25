from sqlalchemy import Column, String, Boolean, DateTime, Integer, BINARY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base, BaseMixin
from typing import Any, Union
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
)


class User(Base, BaseMixin):
    __tablename__ = "user"
    
    name: Union[Any, Column] = Column(String(20), nullable=False, comment="이름")
    nick_name: Union[Any, Column] = Column(String(20), nullable=False, comment="닉네임")
    phone_number: Union[Any, Column] = Column(String(20), unique=True, nullable=False, comment="전화번호")
    email: Union[Any, Column] = Column(String(50), unique=True, nullable=False, comment="이메일")
    password: Union[Any, Column] = Column(String(50), nullable=False, comment="비밀번호")
    
    
    def __repr__(self) -> str:
        return self.name