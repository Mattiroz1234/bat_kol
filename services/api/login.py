from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
users = db["users"]

if users.count_documents({"email": "test@example.com"}) == 0:
    users.insert_one({"email": "test@example.com", "password": "1234"})


class UserRequest(BaseModel):
    email: str
    password: str


@app.post("/register")
def register(data: UserRequest):
    user = users.find_one({"email": data.email})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one({"email": data.email, "password": data.password})
    return {"message": f"User {data.email} registered successfully!"}


@app.post("/login")
def login(data: UserRequest):
    user = users.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Wrong password")

    return {"message": f"Welcome back {data.email}!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)