from typing import Optional
from pydantic import BaseModel, validator, Field
from uuid import UUID
from fastapi.param_functions import Query
from typing import Any, Dict, Optional, List, Union
from app.core.utils.date_utils import KST, D
from datetime import datetime, date as date_type


class GenerationHourBase(BaseModel):
    uuid: Optional[UUID] = Field(
        ..., description="자원 고유ID", example="8e06e881-5c9a-4bd7-a2a0-24694eb375eb"
    )
    date: Optional[date_type] = Field(..., description="등록일자", example="2022-04-06")
    generation_hour: Optional[float] = Field(None, description="발전시간", example="3.1")
    latitude: Optional[float] = Field(
        None, description="위도", example="36.6375346629654"
    )
    longitude: Optional[float] = Field(
        None, description="경도", example="127.459726819858"
    )
    region_code: Optional[str] = Field(..., description="지역 코드", example="4687036023")
    address: Optional[str] = Field(..., description="주소", example="서울시 송파구 문정동")

    class Config:
        orm_mode = True


class ListGenerationHour(BaseModel):
    results: List[GenerationHourBase]


class GenerationHourCreate(GenerationHourBase):
    update_date: Optional[datetime] = Field(
        ..., description="수정일자", example="2022-04-08 09:01:23.507111 +09:00"
    )


class GenerationHour(GenerationHourBase):
    pass
