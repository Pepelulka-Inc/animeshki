from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(router)