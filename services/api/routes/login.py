from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel, Field
from pymongo import MongoClient
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import uvicorn

from common.config import settings

router = APIRouter(prefix="/login",tags=["login"])

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
users = db["users"]

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class TokenRequest(BaseModel):
    token: str = Field(...)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(data: UserRequest = Depends()):
    user = users.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token(
        {"sub": data.email},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token}


@router.post("/register")
def register(data: UserRequest = Depends()):
    user = users.find_one({"email": data.email})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one({"email": data.email, "password": data.password})
    return {"message": f"User {data.email} registered successfully!"}


@router.post("/protected")
def protected(data: TokenRequest = Depends()):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Hello {email}, this is a protected route!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


if __name__ == "__main__":
    uvicorn.run(router, host="127.0.0.1", port=8000)