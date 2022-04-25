from fastapi import APIRouter
from app.api.v1.region.views import resource_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(resource_router, prefix="/members", tags=["회원가입 API"])
