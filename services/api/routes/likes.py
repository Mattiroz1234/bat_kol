from fastapi import APIRouter, HTTPException
from common.config import settings
from common.logger import Logger
from pydantic import BaseModel
from typing import Literal
from common.mongo_client import mongo
from common.kafka_producer import Producer

logger = Logger.get_logger(name=__name__)
router = APIRouter(prefix="/likes",tags=["likes"])
producer = Producer()
feedback_collection = mongo.get_collection(settings.MONGO_COLLECTION_LIKES)
KAFKA_TOPIC = settings.TOPIC_FEEDBACKS

class Feedback(BaseModel):
    actor_id: str
    target_id: str
    status: Literal["likes", "dislikes", "waiting"]

@router.post("/feedback")
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
        try:
            kafka_message = {
                "actor_id": feedback.actor_id,
                "target_id": feedback.target_id,
                "status": feedback.status
            }
            producer.send_message(topic=KAFKA_TOPIC, value=kafka_message)
            producer.flush_producer()
            logger.info(f"Sent feedback to Kafka topic {KAFKA_TOPIC}: {kafka_message}")
        except Exception as e:
            logger.error(f"Error sending feedback to Kafka: {e}")

        return refund
    except Exception as e:
        logger.error(f"Error saving feedback for user {feedback.actor_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))