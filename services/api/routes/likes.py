from fastapi import APIRouter, HTTPException
from common.config import settings
from common.logger import Logger
from pydantic import BaseModel
from typing import Literal
from common.mongo_client import mongo

logger = Logger.get_logger()
likes_router = APIRouter(prefix="/likes",tags=["likes"])

feedback_collection = mongo.get_collection(settings.MONGO_COLLECTION_LIKES)

class Feedback(BaseModel):
    actor_id: str
    target_id: str
    status: Literal["likes", "dislikes", "waiting"]

@likes_router.post("/feedback")
def save_feedback(feedback: Feedback):
    try:
        statuses = ["likes", "dislikes", "waiting"]
        others = [s for s in statuses if s != feedback.status]
        update_query = {"$addToSet": {feedback.status: feedback.target_id},
                        "$pull": {s: feedback.target_id for s in others}}

        result = feedback_collection.update_one(
            {"_id": feedback.actor_id},update_query,upsert=True)
        refund = {
            "status": "success",
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }
        logger.info(f"The update of {feedback.actor_id} was successful:{refund}")
        return refund
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))