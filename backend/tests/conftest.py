import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.main import app
from app.core.utils.date_utils import D
from app.core.common.config import settings
from app.models import UserAuth, User

_db_conn = create_engine(settings.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="function")
def test_app() -> TestClient:
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="session")
def test_db_session() -> Session:
    sess = Session(bind=_db_conn)
    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="function")
def test_auth_number(test_app: TestClient, test_db_session: Session) -> str:
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

    return item.auth_number
