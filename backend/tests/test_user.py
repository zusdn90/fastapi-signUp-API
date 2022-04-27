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


def test_auth_phone_number(test_app: TestClient, test_db_session: Session):
    params = {
        "phone_number": "01000000000",
    }

    response = test_app.post("/v1/register/auth", json=params)
    assert response.status_code == 200

    item = (
        test_db_session.query(UserAuth)
        .filter(UserAuth.phone_number == params["phone_number"])
        .first()
    )
    assert item is not None
    assert item.phone_number == params["phone_number"]
