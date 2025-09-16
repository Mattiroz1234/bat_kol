# matchmaking/common/kafka_producer.py
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
from typing import Optional, Sequence, Tuple
from common.logger import Logger
from common.config import settings

logger = Logger.get_logger(name=__name__)

class Producer:
    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.producer: Optional[KafkaProducer] = None
        brokers = bootstrap_servers or settings.KAFKA_BROKERSS
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=brokers,
                value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
                key_serializer=lambda k: str(k).encode("utf-8") if k is not None else None,
            )
            logger.info(f"KafkaProducer initialized (brokers={brokers})")
        except NoBrokersAvailable:
            logger.error(f"No Kafka brokers available at {brokers}")
        except Exception as e:
            logger.error(f"KafkaProducer init error: {e}")

    @property
    def ready(self) -> bool:
        return self.producer is not None

    def send_message(
        self,
        topic: str,
        value: dict,
        key: Optional[str | int] = None,
        headers: Optional[Sequence[Tuple[str, bytes]]] = None,
        timeout: float = 10.0,
    ) -> bool:
        if not self.producer:
            logger.error("Producer not initialized; message not sent")
            return False
        try:
            fut = self.producer.send(topic, key=key, value=value, headers=headers or [])
            md = fut.get()
            print( f"Kafka → topic={md.topic} partition={md.partition} offset={md.offset}")
            logger.info(
                f"Kafka → topic={md.topic} partition={md.partition} offset={md.offset}"
            )
            return True
        except Exception as e:
            logger.error(f"Kafka send error (topic={topic}): {e}")
            return False

    def flush_producer(self):
        if not self.producer:
            return
        try:
            self.producer.flush()
            self.producer.close()
            logger.info("KafkaProducer flushed & closed")
        except Exception as e:
            logger.error(f"KafkaProducer close error: {e}")
        finally:
            self.producer = None
