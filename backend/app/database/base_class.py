from typing import Any, Union
from datetime import datetime

from sqlalchemy.ext.declarative import as_declarative
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
from sqlalchemy.orm import Session, relationship


@as_declarative()
class Base:
    id: Any
    __name__: str


class BaseMixin:
    id: Union[int, Column] = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    created_date: Union[datetime, None, Column] = Column(
        DateTime(timezone=True), server_default=func.now(), comment="생성일"
    )
    modified_date: Union[datetime, None, Column] = Column(
        DateTime(timezone=True), onupdate=func.now(), comment="수정일"
    )

    def __hash__(self):
        return hash(self.id)

    def all_columns(self):
        return [c for c in self.__table__.columns]  # type:ignore
