# matchmaking/common/kafka_consumer.py
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
from typing import Optional, Iterable
from common.logger import Logger
from common.config import settings

logger = Logger.get_logger(name=__name__)


class Consumer:


    def __init__(
        self,
        topics: Iterable[str],
        group_id: str,
        bootstrap_servers: Optional[str] = None,
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
    ):
        self.consumer: Optional[KafkaConsumer] = None
        brokers = bootstrap_servers or settings.KAFKA_BROKERSS
        try:
            self.consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=brokers,
                group_id=group_id,
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=enable_auto_commit,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                key_deserializer=lambda k: k.decode("utf-8") if k else None,
            )
            logger.info(f"KafkaConsumer subscribed (topics={topics}, group={group_id}, brokers={brokers})")
        except NoBrokersAvailable:
            logger.error(f"No Kafka brokers available at {brokers}")
        except Exception as e:
            logger.error(f"KafkaConsumer init error: {e}")

    @property
    def ready(self) -> bool:
        return self.consumer is not None

    def listen(self):

        if not self.consumer:
            logger.error("Consumer not initialized; cannot listen")
            return
        try:
            for msg in self.consumer:
                yield msg
        except Exception as e:
            logger.error(f"KafkaConsumer listen error: {e}")

    def close(self):
        if not self.consumer:
            return
        try:
            self.consumer.close()
            logger.info("KafkaConsumer closed")
        except Exception as e:
            logger.error(f"KafkaConsumer close error: {e}")
        finally:
            self.consumer = None
