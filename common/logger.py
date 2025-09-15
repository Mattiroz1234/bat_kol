# matchmaking/common/logger.py
import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from .config import settings


class Logger:


    _logger = None

    @classmethod
    def get_logger(cls, name: str = None, level: int = logging.DEBUG):
        if cls._logger:
            return cls._logger

        logger_name = name or settings.SERVICE_NAME or "app"
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        if not logger.handlers:
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)


            if settings.APP_ENV != "dev":
                try:
                    es = Elasticsearch(str(settings.ES_URL))
                    es_index = getattr(settings, "ES_INDEX_LOGGER", "logs")

                    class ESHandler(logging.Handler):
                        def emit(self, record):
                            try:
                                es.index(
                                    index=es_index,
                                    document={
                                        "timestamp": datetime.utcnow().isoformat(),
                                        "level": record.levelname,
                                        "logger": record.name,
                                        "message": record.getMessage(),
                                    },
                                )
                            except Exception as e:
                                print(f"ES log failed: {e}")

                    logger.addHandler(ESHandler())
                except Exception as e:
                    print(f"[Logger] Failed to connect to Elasticsearch: {e}")

            cls._logger = logger

        return logger
