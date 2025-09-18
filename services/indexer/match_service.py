from sentence_transformers import SentenceTransformer
from common.config import settings
from common.logger import Logger
from services.indexer.elastic_service import ElasticService
from services.indexer.mongo_service import MongoService

mongoService = MongoService()
model = SentenceTransformer("all-MiniLM-L6-v2")
logger = Logger.get_logger(name=__name__)

def match_server(profile:dict, topic:list = [settings.TOPIC_PROFILES_CREATEDD]):
    logger.info(f"start consumer listen - topic: {topic}")

    index_name = "female"
    if profile["gender"] == "Male":
        index_name = "male"

    esr = ElasticService(index_name)
    profile_id = profile["unique_id"]

    esr.upsert_doc(
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