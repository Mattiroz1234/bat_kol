# matchmaking/common/mongo_client.py
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Any, Dict, Optional
from common.config import settings
from common.logger import Logger


logger = Logger.get_logger(name=__name__)


class MongoConnection:
    """Simple wrapper around pymongo for our services, with robust logging & error handling."""

    def __init__(self, uri: str = None, db_name: str = None):
        self._uri = uri or str(settings.MONGO_URL)
        self._db_name = db_name or settings.MONGO_DB
        self._client: Optional[MongoClient] = None
        self._db = None
        logger.debug(f"MongoConnection initialized (uri={self._uri}, db={self._db_name})")

    def connect(self):
        if self._client is not None:
            return self._db
        try:
            self._client = MongoClient(self._uri)
            self._db = self._client[self._db_name]
            logger.info(f"Connected to MongoDB at {self._uri}, db={self._db_name}")
            return self._db
        except Exception as e:
            logger.exception(f"Mongo connect failed (uri={self._uri}, db={self._db_name})")
            raise f"Mongo connect failed: {e}"

    def get_collection(self, name: str) -> Collection:
        try:
            if self._db is None:
                self.connect()
            logger.debug(f"Accessing collection: {name}")
            return self._db[name]
        except Exception as e:
            logger.exception(f"Get collection failed (name={name})")
            raise f"Get collection failed ({name}): {e}" from e

    def insert(self, coll: str, doc: Dict[str, Any]) -> str:
        try:
            col = self.get_collection(coll)
            result = col.insert_one(doc)
            _id = str(result.inserted_id)
            logger.info(f"Inserted document into '{coll}' with _id={_id}")
            return _id
        except Exception as e:
            logger.exception(f"Insert failed (coll={coll}, doc_keys={list(doc.keys())})")
            raise Exception(f"Insert failed ({coll}): {e}") from e


    def find_one(self, coll: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            col = self.get_collection(coll)
            result = col.find_one(query)
            logger.debug(f"find_one on '{coll}' with query={query} → {bool(result)}")
            return result
        except Exception as e:
            logger.exception(f"find_one failed (coll={coll}, query={query})")
            raise f"find_one failed ({coll}): {e}" from e

    def update(self, coll: str, query: Dict[str, Any], update: Dict[str, Any]):
        try:
            col = self.get_collection(coll)
            res = col.update_one(query, {"$set": update}, upsert=False)
            logger.info(
                f"update_one on '{coll}' (matched={res.matched_count}, modified={res.modified_count}) "
                f"query={query}, set_keys={list(update.keys())}"
            )
            return res
        except Exception as e:
            logger.exception(f"update failed (coll={coll}, query={query}, update_keys={list(update.keys())})")
            raise f"update failed ({coll}): {e}" from e

    def close(self):
        try:
            if self._client:
                self._client.close()
                logger.info("MongoDB connection closed")
        except Exception as e:
            logger.exception("Mongo close failed")
            raise f"Mongo close failed: {e}" from e
        finally:
            self._client = None
            self._db = None



mongo = MongoConnection()