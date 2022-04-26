from fastapi import APIRouter
from app.api.v1.register import router as register_router
from app.api.v1.user import router as user_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(register_router, prefix="/register", tags=["회원가입 API"])
api_router.include_router(user_router, prefix="/users", tags=["유저 API"])
