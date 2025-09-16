from fastapi import FastAPI
from services.api.routes.add_a_new_person import router as add_person_router
from services.api.routes.likes import router as likes_router
from services.api.routes.login import router as login_router
from services.api.routes.waiting_matches import router as waiting_matches_router


app = FastAPI()

app.include_router(add_person_router)
app.include_router(likes_router)
app.include_router(login_router)
app.include_router(waiting_matches_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)