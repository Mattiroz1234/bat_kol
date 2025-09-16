from sentence_transformers import SentenceTransformer


from common.config import settings
from common.es_client import Elastic
from common.kafka_consumer import Consumer
from services.indexer.elastic_service import ElasticService
from services.indexer.mongo_service import MongoService

mongoService = MongoService()
model = SentenceTransformer("all-MiniLM-L6-v2")

def consumer(topic:list = ["topic_22"], group_id:str = F'group_{"topic_2"}77'):

    cons = Consumer(topic , group_id)
    for profile in cons.listen():
        index_name = "female"
        profile = profile.value
        print(type(profile))
        print(profile)
        if profile["gender"] == "Male":
            index_name = "male"

        es = Elastic(settings.ES_URL, index_name)
        esr = ElasticService(index_name)
        profile_id = profile["unique_id"]
        list_profiles_id = esr.match_search(profile_id)
        mongoService.insert_match(profile_id ,list_profiles_id)

        es.upsert_doc(
            profile["unique_id"],
            {
                    "id" : profile_id,
                    "text_self_vector": model.encode(profile['free_text_self']).tolist(),
                    "text_for_search_vector": model.encode(profile['free_text_for_search']).tolist()
            },
            "true"
        )