from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, Body

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.requests import Request

from app import models, schemas
from app.middlewares.custom_middleware import ExceptionRoute
from app.core.errors.exceptions import CommonException
from app.core.utils.logger import base_logger
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
    "/login/{login_type}",
    status_code=200,
    responses={
        **responses,
        200: {"model": schemas.Token},
    },
    summary="로그인",
)
async def login(
    login_type: schemas.LoginType,
    db: Session = Depends(get_db),
    user: schemas.Login = Body(
        ..., examples=schemas.Login.Config.schema_extra["examples"]
    ),
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
        Authorization=f"JWT {create_access_token(data=schemas.UserToken.from_orm(user_instance).dict(exclude={'password',}),)}"
    )

    return token


@router.post(
    "/",
    responses={
        **responses,
        200: {"model": schemas.UserMe},
    },
    status_code=200,
    summary="유저 토큰 인증",
)
async def get_users(request: Request, db: Session = Depends(get_db)):
    """
    `유저 토큰 인증 API`
    """
    user = request.state.user
    user_instance = (
        db.query(models.User)
        .filter(models.User.phone_number == user.phone_number)
        .first()
    )
    return schemas.UserMe.from_orm(user_instance)


@router.get(
    "/{id}",
    responses={
        **responses,
        200: {"model": schemas.UserMe},
    },
    status_code=200,
    summary="유저 정보 상세조회",
)
async def get_users(id: int, db: Session = Depends(get_db)):
    """
    `유저 정보 상세조회 API`
    """
    user_instance = db.query(models.User).filter(models.User.id == id).first()
    return schemas.UserMe.from_orm(user_instance)
