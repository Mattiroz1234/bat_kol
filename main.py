from fastapi import FastAPI
from services.api.routes.likes import likes_router

app = FastAPI()

app.include_router(likes_router)