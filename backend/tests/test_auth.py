import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.models import UserAuth, User


# def test_insert_data(test_app: TestClient, test_db_session: Session):

#     # insert users auth data (전화번호 인증)
#     auth_instance = UserAuth()
#     auth_instance.phone_number = "01000000000"
#     auth_instance.auth_number = "000000"

#     test_db_session.add(auth_instance)
#     test_db_session.commit()

#     # insert user data
#     user_instance = User()
#     user_instance.name = "테스트"
#     user_instance.nickname = "테테스트"
#     user_instance.email = "test@gmail.com"
#     user_instance.phone_number = "01000000000"
#     user_instance.password = (
#         "$2b$12$96Oi0DzA9bz6pgoxVg4sHeE34yGCAFN37Pm1V.N6vwXTWkQAu5Sx."
#     )

#     test_db_session.add(auth_instance)
#     test_db_session.add(user_instance)
#     test_db_session.commit()


def test_422__auth_phone_number_api(test_app: TestClient, test_db_session: Session):
    params = {
        "phonde_number": "01000000000",
    }

    response = test_app.post("/v1/register/auth", json=params)
    assert response.status_code == 422


def test_400_register_user_api(
    test_app: TestClient, test_db_session: Session, test_auth_number: str
):
    params = {
        "name": "테스트",
        "email": "test@gmail.com",
        "nick_name": "테스트",
        "phone_number": "01000000000",
        "password": "test!!",
        "auth_number": "349234",
    }

    response = test_app.post("/v1/register/", json=params)
    assert response.status_code == 400


def test_422_register_user_api(
    test_app: TestClient, test_db_session: Session, test_auth_number: str
):
    params = {
        "namse": "테스트",
        "emacil": "test@gmail.com",
        "nickvc_name": "테스트",
        "phone_cnumber": "01000000000",
        "password": "test!!",
        "auth_number": test_auth_number,
    }

    response = test_app.post("/v1/register/", json=params)
    assert response.status_code == 422


def test_201_register_user_api(
    test_app: TestClient, test_db_session: Session, test_auth_number: str
):
    # 회원가입 후 로그인 테스트
    register_params = {
        "name": "테스트",
        "email": "test@gmail.com",
        "nick_name": "테스트",
        "phone_number": "01000000000",
        "password": "test!!",
        "auth_number": test_auth_number,
    }

    response = test_app.post("/v1/register/", json=register_params)
    assert response.status_code == 201

    # 전화번호 로그인
    params = {
        "id": register_params["phone_number"],
        "password": register_params["password"],
    }

    response = test_app.post("/v1/users/login/mobile", json=params)
    assert response.status_code == 200

    # 이메일 로그인
    params = {
        "id": register_params["email"],
        "password": register_params["password"],
    }

    response = test_app.post("/v1/users/login/email", json=params)
    assert response.status_code == 200

    test_db_session.query(User).filter(
        User.phone_number == register_params["phone_number"]
    ).delete()
    test_db_session.query(UserAuth).filter(
        UserAuth.phone_number == register_params["phone_number"]
    ).delete()
    test_db_session.commit()
