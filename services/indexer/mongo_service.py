from common.mongo_client import MongoConnection

class MongoService:
    def __init__(self):
        self.mongo_db = MongoConnection()

    def insert_match(self, profile_id, list_profiles_id):
        if self.mongo_db.check_exists_by_id("likes", profile_id):
            self.mongo_db.update(
                "likes",
                {"profile_id": profile_id},
                {"$addToSet": {"waiting": {"$each": list_profiles_id}}}
            )
        else:
            doc = {
                "profile_id" : profile_id,
                "likes" : [],
                "waiting" : list_profiles_id,
                "dislikes" : []
            }
            self.mongo_db.insert('likes',doc)


