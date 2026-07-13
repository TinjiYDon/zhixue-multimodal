from fastapi import APIRouter

from app.api.v1.endpoints import ask, courses, health, upload

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(ask.router, prefix="/courses", tags=["ask"])
