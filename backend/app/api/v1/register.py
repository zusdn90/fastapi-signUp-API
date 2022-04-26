import jwt
import bcrypt
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
    params: schemas.UserPhoneNumberAuth,
    db: Session = Depends(get_db),
):
    """
    `전화번호 인증 API`
    """
    LOGGER.info(f"Parameters : {params}")

    try:
        phone_number = params.phone_number
        auth_instance = db.query(models.UserAuth).filter(phone_number == phone_number)
        auth_instance = auth_instance.first()
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


# @router.post(
#     "/token/auth",
#     status_code=201,
#     responses={
#         **responses,
#         200: {"model": schemas.Token},
#     },
#     summary="토근발급",
# )
# async def register(
#     token: schemas.TokenCreate, db: Session = Depends(get_db)
# ) -> JSONResponse:
#     """
#     `토근생성 API`
#     """
#     phone_number = token.phone_number
#     users = db.query(models.User).filter(phone_number == phone_number)
#     auth_instance = auth_instance.first()


#     if not token.phone_number or not token.password:
#         raise CommonException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Phone Number and PW must be provided.",
#         )
#     if db_user:
#         raise CommonException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Phone Number already registered.",
#         )
#     new_user = crud.create_user(db=db, user=user)
#     token = dict(
#         Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(),)}"
#     )

#     return token


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
        email = create_item["auth_number"]
        name = create_item["name"]
        nick_name = create_item["nick_name"]
        password = create_item["password"]

        # 인증번호 확인
        auth_instance = db.query(models.UserAuth).filter(phone_number == phone_number)
        auth_instance = auth_instance.first()

        if auth_instance.auth_number != auth_number:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not Invalid auth number ...",
            )

        # 사용자 확인
        user_instance = is_user_exist(db=db, phone_number=phone_number)

        if user_instance:
            raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="already existing user...",
            )

        user = models.User()
        user.nick_name = nick_name
        user.email = email
        user.name = name
        user.phone_number = phone_number
        user.password = get_hashed_password(plain_text_password=password)

        token = dict(
            Authorization=f"Bearer {create_access_token(data=schemas.UserCreate.from_orm(user).dict(),)}"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
    except CommonException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    return token


@router.post(
    "/reset/password",
    responses={
        **responses,
        200: {"model": schemas.UserMe},
    },
    status_code=200,
    summary="비밀번호 찾기",
)
async def reset_password(
    params: schemas.UserFindPwd, db: Session = Depends(get_db)
) -> JSONResponse:
    """
    `비밀번호 찾기(재설정) API`\n
    `전화번호 인증 후 비밀번호 재설정`
    """

    auth_instance = db.query(models.UserAuth).filter(phone_number == phone_number)
    auth_instance = auth_instance.first()

    if auth_instance.auth_number == params.auth_number:
        user_instance = models.User()
        user_instance.password = get_hashed_password(
            plain_text_password=params.password
        )
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)

    return user_instance


def is_user_exist(db: Session, phone_number: str):
    user = db.query(models.User).filter(phone_number == phone_number)
    user = user.first()

    if user:
        return True
    return False


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password)


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
