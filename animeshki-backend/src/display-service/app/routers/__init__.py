from fastapi import APIRouter
from routers.register import router as register_router

router = APIRouter()

router.include_router(register_router)
