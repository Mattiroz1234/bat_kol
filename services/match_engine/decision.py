# services/match_engine/app/decision.py
from typing import List, Dict, Literal
from common.logger import Logger
from mongo_reader import MongoReader
from common.config import settings

logger = Logger.get_logger(name=__name__)

  # {"topic": str, "key": str, "value": dict}

class MatchDecider:


    def __init__(self,
                 reader: MongoReader,
                 topic_like: str = "notify.like",
                 topic_match: str = "matches.created"):
        self.reader = reader
        self.topic_like = topic_like
        self.topic_match = topic_match

    def process_feedback(self, msg: Dict[str, str]) ->List:

        actor = msg.get("actor_id")
        target = msg.get("target_id")
        status: Literal["likes", "dislikes", "waiting"] = msg.get("status", "waiting")  # type: ignore

        if not actor or not target:
            logger.warning(f"bad message (missing ids): {msg}")
            return []

        if status != "likes":
            return []

        if self.reader.has_blocking_dislike(actor, target):
            logger.info(f"blocked by dislike: {actor} - {target}")
            return []


        if self.reader.has_mutual_like(actor, target):
            logger.info(f"match! {actor} - {target}")
            return [
                {"topic": self.topic_match, "key": actor,
                 "value": {"user_id": actor, "partner_id": target, "reason": "mutual_like"}},
                {"topic": self.topic_match, "key": target,
                 "value": {"user_id": target, "partner_id": actor, "reason": "mutual_like"}},
            ]


        logger.info(f"single like {actor} → {target}")
        return [
            {"topic": self.topic_like, "key": target,
             "value": {"user_id": target, "from_user_id": actor, "reason": "single_like"}}
        ]


