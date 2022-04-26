import jwt
from random import randint
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, Body

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import models, schemas
from app.core.utils.date_utils import D
from app.middlewares.custom_middleware import ExceptionRoute
from app.core.errors.exceptions import CommonException
from app.core.utils.logger import base_logger
from app.core.common.consts import JWT_SECRET, JWT_ALGORITHM
from app.database.session import get_db
from app.database import crud

LOGGER = base_logger()
router = APIRouter(route_class=ExceptionRoute)


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Exception raised."},
        }


responses = {
    400: {"model": HTTPError, "description": "Bad request"},
    500: {"model": HTTPError, "description": "Internal server error"},
}


@router.post(
    "/login",
    status_code=200,
    summary="로그인",
)
async def login(db: Session = Depends(get_db)) -> JSONResponse:
    """
    `로그인 API`
    """

    return ""


@router.get(
    "/",
    status_code=200,
    summary="회원정보 조회",
)
async def users_info(db: Session = Depends(get_db)) -> JSONResponse:
    """
    `회원정보 조회 API`
    """

    return ""
