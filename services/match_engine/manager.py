from common.config import settings
from common.logger import Logger
from common.kafka_consumer import Consumer
from common.kafka_producer import Producer

from mongo_reader import MongoReader
from decision import MatchDecider

logger = Logger.get_logger(name=__name__)

INPUT_TOPIC        = getattr(settings, "TOPIC_FEEDBACKS", "feedbacks")
OUTPUT_TOPIC_LIKE  = getattr(settings, "TOPIC_NOTIFY_LIKE", "notify.like")
OUTPUT_TOPIC_MATCH = getattr(settings, "TOPIC_MATCHES", "matches.created")
GROUP_ID           = getattr(settings, "KAFKA_GROUP_MATCH_ENGINE", "match_engine")



COLLECTION_NAME = getattr(settings, "MONGO_COLL_LIKES", "likes")
ID_FIELD        = getattr(settings, "PROFILE_ID_FIELD", "profile_id")
LIKES_FIELD     = getattr(settings, "LIKES_FIELD", "likes")
DISLIKES_FIELD  = getattr(settings, "DISLIKES_FIELD", "dislikes")

reader  = MongoReader(COLLECTION_NAME, id_field=ID_FIELD,likes_field=LIKES_FIELD, dislikes_field=DISLIKES_FIELD)
decider = MatchDecider(reader, topic_like=OUTPUT_TOPIC_LIKE, topic_match=OUTPUT_TOPIC_MATCH)

consumer = Consumer(topics=[INPUT_TOPIC], group_id=GROUP_ID, enable_auto_commit=True)
producer = Producer()

def process_messages():
    if not consumer.ready:
        logger.error("Consumer not ready, exiting")
        return
    try:
        for msg in consumer.listen():
            logger.info(f"Received message: {msg.value}")
            feedback = msg.value
            if not isinstance(feedback, dict):
                logger.warning(f"Invalid message format, expected dict but got {type(feedback)}")
                continue
            actions = decider.process_feedback(feedback)
            for action in actions:
                success = producer.send_message(
                    topic=action['topic'],
                    value=action['value'],
                    key=action.get('key')
                )
                if success:
                    logger.info(f"Sent message to {action['topic']}: {action['value']}")
                else:
                    logger.error(f"Failed to send message to {action['topic']}: {action['value']}")
    except Exception as e:
        logger.error(f"Error processing messages: {e}")
    finally:
        try:
            producer.flush_producer()
        except Exception as e:
            logger.error(f"Error flushing producer: {e}")
        try:
            consumer.close()
        except Exception as e:
            logger.error(f"Error closing consumer: {e}")
