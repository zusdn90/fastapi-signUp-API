import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends,status

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.middlewares.custom_middleware import ExceptionRoute

from app.core.errors.exceptions import CommonException
from app.core.utils.logger import base_logger
from app.core.common.consts import JWT_SECRET, JWT_ALGORITHM
from app.database.session import get_db
from app.models import User
from app.database import crud
from app.schemas import Token, UserToken, UserCreate

LOGGER = base_logger()
user_router = APIRouter(route_class=ExceptionRoute)


@user_router.post("/", status_code=201, response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> JSONResponse:
    """
    `회원가입 API`\n
    :return:
    """
    db_user = crud.get_user_by_phone_number(db, phone_number=user.phone_number)
    
    if not user.phone_number or not user.password:
        raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number and PW must be provided."
            )
    if db_user:
        raise CommonException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already registered."
            )
    new_user = crud.create_user(db=db, user=user)
    token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(),)}")
    
    return token


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt