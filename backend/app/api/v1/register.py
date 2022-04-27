from random import randint
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, Body

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import models, schemas
from app.middlewares.custom_middleware import ExceptionRoute
from app.core.errors.exceptions import CommonException
from app.core.utils.logger import base_logger
from app.database.session import get_db
from app.api.v1.helper import (
    is_user_exist,
    is_auth_exist,
    get_hashed_password,
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
    "/auth",
    responses={
        **responses,
        200: {"model": schemas.AuthNumber},
    },
    status_code=200,
    summary="전화번호 인증",
)
async def mobile_auth(
    params: schemas.UserPhoneNumber,
    db: Session = Depends(get_db),
):
    """
    `전화번호 인증 API`
    """
    LOGGER.info(f"Parameters : {params}")

    try:
        phone_number = params.phone_number

        auth_instance = is_auth_exist(db=db, phone_number=phone_number)
        auth_number = str(randint(100000, 500000))

        if phone_number == "" or phone_number is None:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone Number must be provided...",
            )

        if auth_instance:
            auth_instance.auth_number = auth_number
            db.add(auth_instance)
        else:
            auth = models.UserAuth()
            auth.phone_number = phone_number
            auth.auth_number = auth_number
            db.add(auth)

        db.commit()
    except CommonException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    return schemas.AuthNumber(auth_number=auth_number)


@router.post(
    "/",
    status_code=201,
    responses={
        **responses,
        200: {"model": schemas.Token},
    },
    summary="회원가입",
)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    `회원가입 API`
    """
    create_item = user.dict(exclude_unset=True)  # 세팅되지 않은 파라미터 값 제외

    try:
        phone_number = create_item["phone_number"]
        auth_number = create_item["auth_number"]
        email = create_item["email"]
        name = create_item["name"]
        nick_name = create_item["nick_name"]
        password = create_item["password"]

        # 인증번호 확인
        auth_instance = is_auth_exist(db=db, phone_number=phone_number)

        if not auth_instance:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=" Invalid verification Phone number...",
            )

        if auth_instance.auth_number != auth_number:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification auth number ...",
            )

        # 사용자 확인
        is_phone_number = is_user_exist(db=db, _id=phone_number)
        is_email = is_user_exist(db=db, _id=email, login_type="email")

        if is_phone_number or is_email:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="already existing user...",
            )

        user_instance = models.User()
        user_instance.nick_name = nick_name
        user_instance.email = email
        user_instance.name = name
        user_instance.phone_number = phone_number
        user_instance.password = get_hashed_password(plain_text_password=password)

        if user_instance:
            db.add(user_instance)
            db.commit()
            db.refresh(user_instance)
        else:
            db.rollback()

    except CommonException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    token = dict(
        Authorization=f"JWT {create_access_token(data=schemas.UserToken.from_orm(user_instance).dict(exclude={'password',}),)}"
    )

    return token


@router.post(
    "/reset/password",
    responses={
        **responses,
        200: {"model": schemas.UserMe},
    },
    status_code=200,
    summary="비밀번호 찾기(재설정)",
)
async def reset_password(
    params: schemas.UserFindPwd, db: Session = Depends(get_db)
) -> JSONResponse:
    """
    `비밀번호 찾기(재설정) API`\n
    `전화번호 인증 후 비밀번호 재설정`
    """

    try:
        auth_instance = is_auth_exist(db=db, phone_number=params.phone_number)

        if not auth_instance:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=" Invalid verification Phone number...",
            )

        if auth_instance.auth_number == params.auth_number:
            user_instance = (
                db.query(models.User)
                .filter(models.User.phone_number == params.phone_number)
                .first()
            )

            user_instance.password = get_hashed_password(
                plain_text_password=params.password
            )
            db.add(user_instance)
            db.commit()
            db.refresh(user_instance)
        else:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=" Invalid verification Auth number...",
            )

    except CommonException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    return schemas.UserMe.from_orm(user_instance)
