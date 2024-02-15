from fastapi import APIRouter

from app.api.api_v1.endpoints import home_router
from app.api.api_v1.endpoints import document_router

api_router = APIRouter()
api_router.include_router(home_router.router, tags=["Home"])
api_router.include_router(document_router.router, tags=["Documents"])
