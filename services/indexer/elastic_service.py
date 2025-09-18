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

    def match_search(self, doc_id, size: int = 1, filters: dict = None):
        doc = self.es.get_doc(doc_id)
        if not doc:
            logger.warning(f"No document found for id {doc_id} in index {self.index}")
            return

        index_gender = "female" if self.index == "male" else "male"

        text_self_vector = doc["text_self_vector"]
        text_for_search_vector = doc["text_for_search_vector"]

        base_query = {"match_all": {}}

        if filters:
            must_filters = []
            must_not_filters = []

            # must
            for field, value in filters.get("include", {}).items():
                if isinstance(value, list):
                    must_filters.append({"terms": {field: value}})
                elif isinstance(value, dict): # range
                    must_filters.append({"range": {field: value}})
                else:
                    must_filters.append({"term": {field: value}})

            # not_must
            for field, value in filters.get("exclude", {}).items():
                if isinstance(value, list):
                    must_not_filters.append({"terms": {field: value}})
                elif isinstance(value, dict): # range
                    must_not_filters.append({"range": {field: value}})
                else:
                    must_not_filters.append({"term": {field: value}})

            base_query = {
                "bool": {
                    "filter": must_filters,
                    "must_not": must_not_filters
                }
            }

        resp = self.es.search(
            index=index_gender,
            query={
                "script_score": {
                    "query": base_query,
                    "script": {
                        "source": """
                            double score1 = cosineSimilarity(params.query_offer_vector, 'text_for_search_vector');
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

        list_profile_id = [hit["_id"] for hit in resp["hits"]["hits"]]
        return list_profile_id