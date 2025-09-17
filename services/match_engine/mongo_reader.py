from common.config import settings
from common.logger import Logger
from common.mongo_client import mongo

logger  = Logger.get_logger(name=__name__)

class MongoReader:
    def __init__(self, collection_name: str, id_field: str = "_id",
                 likes_field: str = "likes", dislikes_field: str = "dislikes"):
        self.collection = mongo.get_collection(collection_name)
        self.id_field = id_field
        self.likes_field = likes_field
        self.dislikes_field = dislikes_field
        logger.info(f"MongoReader ready (coll='{collection_name}', id='{id_field}', likes='{likes_field}', dislikes='{dislikes_field}')")

    def has_mutual_like(self, actor_id: str, target_id: str) -> bool:

        doc = self.collection.find_one({self.id_field: target_id, self.likes_field: actor_id}, {self.id_field: 1})
        return doc is not None

    def has_blocking_dislike(self, actor_id: str, target_id: str) -> bool:

        doc = self.collection.find_one({self.id_field: target_id, self.dislikes_field: actor_id}, {self.id_field: 1})
        return doc is not None






