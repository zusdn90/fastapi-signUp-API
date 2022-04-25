import traceback
import requests

from doctest import Example
from typing import List, Dict
from pydantic import BaseModel, ValidationError
from humps.main import camelize
from fastapi import APIRouter, Header, Path, Depends, status, Query
from fastapi.responses import JSONResponse

from app.middlewares.custom_middleware import ExceptionRoute
from app import models, schemas
from app.core.utils.logger import base_logger
from app.core.utils.date_utils import D
from app.core.common import constants
from app.core.errors.exceptions import CommonException, NotFoundException
from app.database.session import get_db


LOGGER = base_logger()
resource_router = APIRouter(route_class=ExceptionRoute)


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
