from sentence_transformers import SentenceTransformer
from common.config import settings
from common.es_client import Elastic
from common.kafka_consumer import Consumer
from common.logger import Logger
from services.indexer.elastic_service import ElasticService
from services.indexer.mongo_service import MongoService

mongoService = MongoService()
model = SentenceTransformer("all-MiniLM-L6-v2")
logger = Logger.get_logger(name=__name__)
def consumer(topic:list = [settings.TOPIC_PROFILES_CREATEDD], group_id:str = F'group_{settings.TOPIC_PROFILES_CREATEDD}'):

    cons = Consumer(topic , group_id)
    logger.info(f"start consumer - topic: {topic}")
    for profile in cons.listen():
        logger.info(f"start consumer listen - topic: {topic}")

        index_name = "female"
        profile = profile.value
        if profile["gender"] == "Male":
            index_name = "male"

        es = Elastic(settings.ES_URL, index_name)
        esr = ElasticService(index_name)
        profile_id = profile["unique_id"]

        es.upsert_doc(
            profile["unique_id"],
            {
                    "id" : profile_id,
                    "text_self_vector": model.encode(profile['free_text_self']).tolist(),
                    "text_for_search_vector": model.encode(profile['free_text_for_search']).tolist()
            },
            "true"
        )
        logger.debug(f"debug 1, consumer listen - topic: {topic}")

        list_profiles_id = esr.match_search(profile_id)
        mongoService.insert_match(profile_id ,list_profiles_id)

        logger.debug(f"debug 2, consumer listen - topic: {topic}")
        for profile_match in list_profiles_id:
            mongoService.insert_match(profile_match , [profile_id])
