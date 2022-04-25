import time
from starlette.requests import Request
from typing import Callable, List
from app.core.utils.logger import base_logger, api_logger
from app.core.utils.date_utils import D

from fastapi import Body, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

LOGGER = base_logger()


class ExceptionRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as ex:

                if isinstance(ex, RequestValidationError):
                    body = await request.body()
                    detail = {"errors": ex.errors(), "body": body.decode()}
                    LOGGER.exception("RequestValidationError", detail)
                    raise HTTPException(status_code=422, detail=detail)

                if isinstance(ex, HTTPException):
                    raise ex

                LOGGER.exception("uncaught error")
                raise HTTPException(status_code=500, detail=str(ex))

        return custom_route_handler


async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None
    ip = (
        request.headers["x-forwarded-for"]
        if "x-forwarded-for" in request.headers.keys()
        else request.client.host
    )
    if ip:
        request.state.ip = ip.split(",")[0] if "," in ip else ip
    else:
        request.state.ip = None

    response = await call_next(request)
    await api_logger(request=request, response=response)

    return response
