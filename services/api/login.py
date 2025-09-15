from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import uvicorn

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
users = db["users"]

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserRequest(BaseModel):
    email: str
    password: str


class TokenRequest(BaseModel):
    token: str


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login")
def login(data: UserRequest):
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


@app.post("/register")
def register(data: UserRequest):
    user = users.find_one({"email": data.email})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one({"email": data.email, "password": data.password})
    return {"message": f"User {data.email} registered successfully!"}


@app.post("/protected")
def protected(data: TokenRequest):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Hello {email}, this is a protected route!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)