# matchmaking/common/elastic_client.py
from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import bulk
from common.logger import Logger
from common.config import settings

logger = Logger.get_logger(name=__name__)


class Elastic:


    def __init__(self, url: Optional[str] = None, index_name: Optional[str] = None, timeout: int = 30,
                 mapping: Optional[Dict[str, Any]] = None, create_if_missing: bool = True):
        self.url = str(url or settings.ES_URL)
        self.index_name = index_name or settings.ES_INDEX_PROFILES
        self.timeout = timeout

        try:
            self.es = Elasticsearch(self.url, request_timeout=self.timeout)
            if not self.es.ping():
                logger.error("Elasticsearch ping failed")
                raise exceptions.ConnectionError("Elasticsearch is not responding")

            if create_if_missing and not self.es.indices.exists(index=self.index_name):
                logger.info(f"Index '{self.index_name}' not found. Creating...")
                if mapping:
                    self.es.indices.create(index=self.index_name, **mapping)
                else:
                    self.es.indices.create(index=self.index_name)
                logger.info(f"Index '{self.index_name}' created")
        except Exception as e:
            logger.exception(f"Failed to init Elasticsearch: {e}")
            raise

    # ---------- helpers ----------
    def is_exists(self, doc_id: str) -> bool:
        try:
            return bool(self.es.exists(index=self.index_name, id=doc_id))
        except Exception as e:
            logger.error(f"exists({doc_id}) error: {e}")
            return False

    def get_doc(self, doc_id: str, source_includes: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        try:
            resp = self.es.get(index=self.index_name, id=doc_id, _source_includes=source_includes, ignore=[404])
            if not resp or not resp.get("found"):
                return None
            return resp["_source"]
        except Exception as e:
            logger.error(f"get_doc({doc_id}) error: {e}")
            return None

    # ---------- CRUD ----------
    def index_doc(self, doc: Dict[str, Any], doc_id: Optional[str] = None, refresh: Optional[str] = None):
        try:
            resp = self.es.index(index=self.index_name, id=doc_id, document=doc, refresh=refresh)
            logger.info(f"Indexed doc id={resp.get('_id')}")
            return resp
        except Exception as e:
            logger.error(f"index_doc failed: {e}")
            return None

    def upsert_doc(self, doc_id: str, doc: Dict[str, Any], refresh: Optional[str] = None):
        """עדכון/יצירה אם לא קיים (upsert)."""
        try:
            resp = self.es.update(index=self.index_name, id=doc_id, doc=doc, doc_as_upsert=True, refresh=refresh)
            logger.info(f"Upserted doc id={doc_id}")
            return resp
        except Exception as e:
            logger.error(f"upsert_doc failed: {e}")
            return None

    def update_doc(self, doc_id: str, new_values: Dict[str, Any], refresh: Optional[str] = None,
                   doc_as_upsert: bool = False):
        try:
            resp = self.es.update(index=self.index_name, id=doc_id, doc=new_values,
                                  doc_as_upsert=doc_as_upsert, refresh=refresh)
            logger.info(f"Updated doc id={doc_id}")
            return resp
        except Exception as e:
            logger.error(f"update_doc failed: {e}")
            return None

    def delete_documents_by_id(self, ids: List[str], refresh: Optional[str] = None) -> bool:
        try:
            actions = ({"_op_type": "delete", "_index": self.index_name, "_id": _id} for _id in ids)
            success, errors = bulk(self.es, actions, raise_on_error=False)
            if errors:
                logger.error(f"bulk delete had errors: {errors[:3]}... (total={len(errors)})")
            if refresh:
                self.es.indices.refresh(index=self.index_name)
            logger.info(f"Deleted {success} docs (requested {len(ids)})")
            return True
        except Exception as e:
            logger.error(f"delete_documents_by_id failed: {e}")
            return False

    def update_docs(self, docs_to_update: List[Tuple[str, Dict[str, Any]]], refresh: Optional[str] = None) -> bool:
        """
        docs_to_update = [(doc_id, {'field': 'val'}), ...]
        """
        try:
            actions = [
                {"_op_type": "update", "_index": self.index_name, "_id": doc_id, "doc": fields}
                for doc_id, fields in docs_to_update
            ]
            success, errors = bulk(self.es, actions, raise_on_error=False)
            if errors:
                logger.error(f"bulk update had errors: {errors[:3]}... (total={len(errors)})")
            if refresh:
                self.es.indices.refresh(index=self.index_name)
            logger.info(f"Bulk updated {success} docs (requested {len(docs_to_update)})")
            return True
        except Exception as e:
            logger.error(f"update_docs failed: {e}")
            return False

    def search(self, index, query=None, knn=None, size=3):
        try:
            if knn:
                return self.es.search(index=index, knn=knn, size=size)
            elif query:
                return self.es.search(index=index, query=query, size=size)
        except Exception as e:
            logger.error(f"search failed: {e}")

    # ---------- Query ----------
    def count(self) -> int:
        try:
            resp = self.es.count(index=self.index_name)
            return int(resp.get("count", 0))
        except Exception as e:
            logger.error(f"count error: {e}")
            return 0


    # ---------- lifecycle ----------
    def close(self):
        try:
            self.es.transport.close()
            logger.info("Elasticsearch client closed")
        except Exception as e:
            logger.error(f"close error: {e}")
