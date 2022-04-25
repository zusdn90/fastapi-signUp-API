from fastapi import APIRouter
from app.api.v1.users import user_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(user_router, prefix="/users", tags=["회원가입 API"])
