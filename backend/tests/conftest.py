import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.main import app
from app.core.utils.date_utils import D
from app.core.common.config import settings

_db_conn = create_engine(settings.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="function")
def test_app() -> TestClient:
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="session")
def test_db_session():
    sess = Session(bind=_db_conn)
    try:
        yield sess
    finally:
        sess.close()
