from sqlalchemy import Column, String, Boolean, DateTime, Integer, BINARY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base_class import Base, BaseMixin
from datetime import datetime

from typing import Any, Union


class User(Base, BaseMixin):
    __tablename__ = "users"
    
    user_id: Union[Any, Column] = Column(String(100), unique=True, comment="사용자 ID")
    name: Union[Any, Column] = Column(String(20), nullable=False)
    email: Union[Any, Column] = Column(String(50), nullable=False)
    password: Union[Any, Column] = Column(StString(50)ring, nullable=False)
    
    def __repr__(self) -> str:
        return self.name
