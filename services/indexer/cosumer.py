from sentence_transformers import SentenceTransformer
from common.config import settings
from common.kafka_consumer import Consumer
from common.logger import Logger
from services.indexer.match_service import match_server
from services.indexer.mongo_service import MongoService

mongoService = MongoService()
model = SentenceTransformer("all-MiniLM-L6-v2")
logger = Logger.get_logger(name=__name__)
def consumer(topic:list = [settings.TOPIC_PROFILES_CREATEDD], group_id:str = F'group_{settings.TOPIC_PROFILES_CREATEDD}'):

    cons = Consumer(topic , group_id)
    logger.info(f"start consumer - topic: {topic}")
    for profile in cons.listen():
        logger.info(f"start consumer listen - topic: {topic}")
        match_server(profile.value)
