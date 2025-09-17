from fastapi import APIRouter, HTTPException
from common.mongo_client import mongo
from common.config import settings
from common.logger import Logger

logger = Logger.get_logger(name=__name__)
router = APIRouter(prefix="/waiting_matches", tags=["waiting_matches"])

feedback_collection = mongo.get_collection(settings.MONGO_COLLECTION_LIKES)
profiles_collection = mongo.get_collection(settings.MONGO_COLL_PROFILESS)

@router.get("/{actor_id}")
def get_waiting_matches(actor_id: str):
    try:
        user_doc = feedback_collection.find_one({"_id": actor_id}, {"waiting": 1, "_id": 0})
        if not user_doc:
            logger.info(f"User {actor_id} not found in feedback collection.")
            raise HTTPException(status_code=404, detail="User not found")
        waiting_ids = user_doc.get("waiting", [])
        if not waiting_ids:
            logger.info(f"User {actor_id} has no waiting matches.")
            return {"waiting": []}

        cursor = profiles_collection.find(
            {"_id": {"$in": waiting_ids}},
            {"_id": 1, "first_name": 1, "last_name": 1, "age": 1, "gender": 1, "location": 1})
        profiles = [{"id":doc["_id"], **{k: v for k, v in doc.items() if k != "_id"}}
                    for doc in cursor]
        logger.info(f"Found {len(profiles)} waiting matches for user {actor_id}.")
        return {"waiting": profiles}

    except Exception as e:
        logger.error(f"Error retrieving waiting matches for user {actor_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))