from fastapi import FastAPI, Request, Response
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html# type:ignore
from app.core.event_handlers import start_app_handler, stop_app_handler
from app.core.utils.logger import base_logger
from app.api.router import api_router

from fastapi_utils.timing import add_timing_middleware
from app.middlewares.custom_middleware import access_control
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

LOGGER = base_logger()


def get_app() -> FastAPI:
    fast_app = FastAPI(
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )

    # middleware 추가
    add_timing_middleware(fast_app, record=LOGGER.info)
    fast_app.add_middleware(
        middleware_class=TrustedHostMiddleware,
        allowed_hosts=["*"],
        except_path=["/openapi.json", "/docs", "/redoc", "/health"],
    )
    fast_app.add_middleware(
        middleware_class=BaseHTTPMiddleware, dispatch=access_control
    )
    fast_app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # event handler 설정
    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    # route 설정
    fast_app.include_router(api_router)

    return fast_app


app = get_app()


@app.get("/health", summary="API 서버 상태체크")
def get_health():
    """
    ### API 서버 상태체크
    """
    return {"message": "OK"}


@app.get("/docs", include_in_schema=False)
async def access_documentation():
    openapi_url = app.root_path + "/openapi.json"
    return get_swagger_ui_html(openapi_url=openapi_url, title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def access_openapi(request: Request, response: Response):

    openapi = get_openapi(
        title=app.title,
        version=app.version,
        description="",
        routes=app.routes,
        tags=app.openapi_tags,
    )
    openapi["servers"] = [{"url": app.root_path}]
    monkey_patched_openapi = {
        key: value for key, value in openapi.items() if key != "paths"
    }
    monkey_patched_openapi["paths"] = {}
    for key, value in openapi["paths"].items():
        monkey_patched_openapi["paths"][key] = value

    return monkey_patched_openapi
