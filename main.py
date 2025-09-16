from fastapi import FastAPI
from services.api.routes.likes import likes_router
from services.api.routes.waiting_matches import waiting_matches_router

app = FastAPI()

app.include_router(likes_router)
app.include_router(waiting_matches_router)