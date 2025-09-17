from fastapi import UploadFile, File, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from common.mongo_client import MongoConnection
from common.kafka_producer import Producer
from common.config import settings
from common.logger import Logger
import base64
import uvicorn

from services.tools.create_hash import CreateHash

logger = Logger.get_logger(name=__name__)
mongo = MongoConnection()
create_hash = CreateHash()
producer = Producer()

router = APIRouter(prefix="/add_person",tags=["add_person"])
database = {}


class PersonModel(BaseModel):
    email: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    age: int = Field(..., ge=18, le=120)
    location: str = Field(...)
    gender: Literal["Male", "Female"]
    marital_status: Literal["Single", "Divorced", "Widower"]
    origin: Literal["ספרדי", "אשכנזי", "תימני"]
    sector: Literal["חסידי", "ליטאי", "ספרדי"]
    free_text_self: str
    free_text_for_search: str
    occupation: Optional[str] = None
    favorites: Optional[List[str]] = None
    height: Optional[int] = None



async def build_person(person: PersonModel, file: Optional[UploadFile] = File(None)):
    data = person.dict()
    if file:
        contents = await file.read()
        data["photo"] = base64.b64encode(contents).decode("utf-8")
    else:
        data["photo"] = None
    return data


@router.post("/add_person")
async def add_person(person: PersonModel = Depends(), file: Optional[UploadFile] = File(None)):
    person_data = await build_person(person, file)
    person_id = create_hash.made_a_hash(person.email)
    if mongo.check_exists_by_id(settings.MONGO_COLL_PROFILES, person_id):
        logger.error(f"error:{person.email} already exists in the system !!!")
        return {"error": f"{person.email} already exists in the system !!!"}

    logger.info("create a id")
    mongo.insert(settings.MONGO_COLL_PROFILES, {"unique_id": person_id, **person_data} ,person_id)
    logger.info(f"inserted to mongo {settings.MONGO_COLL_PROFILES} collection :")

    person_to_kafka = {"unique_id":person_id,**person_data}
    producer.send_message(settings.TOPIC_PROFILES_CREATEDD,person_to_kafka)
    logger.info(f"send to kafka in {settings.TOPIC_PROFILES_CREATEDD} topic::")
    return JSONResponse({"status": "ok", "person_id": person_id})


@router.get("/people")
def get_people():
    all_collection = mongo.get_collection(settings.MONGO_COLL_PROFILES)
    return all_collection


if __name__ == "__main__":
    uvicorn.run("add_a_new_person:router", host="127.0.0.1", port=8000, reload=True)
