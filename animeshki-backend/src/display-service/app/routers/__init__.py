from fastapi import APIRouter
from routers.register import router as register_router
from routers.login import router as login_router
from routers.home import router as home_router
from routers.search import router as search_router
from routers.anime import router as anime_router
from routers.favorites import router as favorites_router

router = APIRouter()

router.include_router(register_router)
router.include_router(login_router)
router.include_router(home_router)
router.include_router(search_router)
router.include_router(anime_router)
router.include_router(favorites_router)