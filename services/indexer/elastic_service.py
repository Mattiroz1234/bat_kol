from common.es_client import Elastic
from common.config import settings
from common.logger import Logger

logger = Logger.get_logger(name=__name__)

class ElasticService:
    def __init__(self, index_name):
        self.index = index_name
        self.es = Elastic(settings.ES_URL, index_name)

    def upsert_doc(self, doc_id: str, doc: dict,refresh:str):
        self.es.upsert_doc(
            doc_id=doc_id,
            doc=doc,
            refresh=refresh
        )

    def match_search(self,doc_id, size:int = 1):

        doc = self.es.get_doc(doc_id)
        if not doc:
            logger.warning(f"No document found for id {doc_id} in index {self.index}")
            return
        index_gender = "female" if self.index == "male" else "male"

        text_self_vector = doc["text_self_vector"]
        text_for_search_vector = doc["text_for_search_vector"]

        resp = self.es.search(
            index=index_gender,
            query={
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": """
                            // self-text similarity versus text search
                            double score1 = cosineSimilarity(params.query_offer_vector, 'text_for_search_vector');
                            // text search similarity versus self-text
                            double score2 = cosineSimilarity(params.query_search_vector, 'text_self_vector');
                            return score1 + score2 + 1.0;
                        """,
                        "params": {
                            "query_offer_vector": text_self_vector,
                            "query_search_vector": text_for_search_vector
                        }
                    }
                }
            },
            size=size
        )

        list_profile_id =[]
        for hit in resp["hits"]["hits"]:
            list_profile_id.append(hit['_id'])

        return list_profile_id