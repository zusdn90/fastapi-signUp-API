import jwt
import bcrypt

from sqlalchemy.orm import Session
from app import models, schemas
from app.core.common.consts import JWT_SECRET, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES


def is_user_exist(db: Session, _id: str, login_type="phone_number"):
    if login_type == "phone_number":
        user = db.query(models.User).filter(models.User.phone_number == _id)
        user = user.first()
    else:
        user = db.query(models.User).filter(models.User.email == _id)
        user = user.first()

    return user


def is_auth_exist(db: Session, phone_number: str):
    auth_instance = db.query(models.UserAuth).filter(
        models.UserAuth.phone_number == phone_number
    )
    auth_instance = auth_instance.first()

    return auth_instance


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(
        plain_text_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    *, data: dict = None, expires_delta: int = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
