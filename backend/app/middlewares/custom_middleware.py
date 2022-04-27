import time
import jwt
import re

from typing import Callable
from fastapi import Body, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse

from app.core.utils.logger import base_logger, api_logger
from app.core.utils.date_utils import D
from app.core.common import consts
from app.core.errors.exceptions import NotAuthorized, APIException
from app.schemas import UserToken

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

    headers = request.headers
    cookies = request.cookies

    url = request.url.path
    if (
        await url_pattern_check(url, consts.EXCEPT_PATH_REGEX)
        or url in consts.EXCEPT_PATH_LIST
    ):
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    try:
        # JWT 토큰 확인
        if "authorization" in headers.keys():
            token_info = await token_decode(access_token=headers.get("Authorization"))
            request.state.user = UserToken(**token_info)
        else:
            if "Authorization" not in headers.keys():
                raise NotAuthorized()

        response = await call_next(request)
        await api_logger(request=request, response=response)
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(
            status=error.status_code,
            msg=error.msg,
            detail=error.detail,
            code=error.code,
        )
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)

    return response


async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("JWT ", "")
        payload = jwt.decode(
            access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM]
        )
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False
