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
from app.api.v1.helper import (
    is_user_exist,
    get_hashed_password,
    verify_password,
    create_access_token,
)

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
    "/login/{schemas.LoginType}",
    status_code=200,
    responses={
        **responses,
        200: {"model": schemas.Token},
    },
    summary="로그인",
)
async def login(
    login_type: schemas.LoginType, user: schemas.Login, db: Session = Depends(get_db)
):
    """
    `로그인 API`
    """
    _id = user.id
    password = user.password

    try:
        if not _id or not password:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID and PW must be provided...",
            )

        if login_type == login_type.email:
            user_instance = is_user_exist(db=db, _id=_id, login_type=login_type.email)
        else:
            user_instance = is_user_exist(db=db, _id=_id)

        if not user_instance:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NO MATCH USER",
            )

        is_verified = verify_password(
            plain_text_password=password, hashed_password=user_instance.password
        )

        if not is_verified:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NO MATCH USER",
            )
    except CommonException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    token = dict(
        Authorization=f"Bearer {create_access_token(data=schemas.Login.from_orm(user_instance).dict(exclude={'password',}),)}"
    )

    return token


@router.get(
    "/{id}",
    responses={
        **responses,
        200: {"model": schemas.UserMe},
    },
    status_code=200,
    summary="회원정보 조회",
)
async def get_users(_id: int, db: Session = Depends(get_db)):
    """
    `회원정보 조회 API`
    """
    user_instance = db.query(models.User).filter(models.User.id == _id).first()
    return schemas.UserMe.from_orm(user_instance)
