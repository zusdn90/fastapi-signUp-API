import pytest
import uuid
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.main import app
from app.schemas import GenerationHourCreate
from app.core.utils.date_utils import D
from datetime import datetime


@pytest.fixture(scope="function")
def test_app() -> TestClient:
    with TestClient(app=app) as client:
        yield client
