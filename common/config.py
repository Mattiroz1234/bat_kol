# matchmaking/common/config.py
from __future__ import annotations
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class AppSettings(BaseSettings):
    """App-level settings shared by all services."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ---- MongoDB ----
    MONGO_URL: AnyUrl = Field("mongodb://mongo:27017", description="Mongo connection string")
    MONGO_DB: str = Field("matchmaking", description="Mongo database name")
    MONGO_COLLECTION_LIKES: str = Field("likes", description="likes collection name")

    # ---- Elasticsearch ----
    ES_URL: AnyUrl = Field("http://elasticsearch:9200", description="Elasticsearch base URL")
    ES_INDEX_PROFILES: str = Field("profiles_v1", description="Profiles index name")
    ES_ALIAS_PROFILES: str = Field("profiles_active", description="Alias for blue/green")

    # ---- Kafka ----
    KAFKA_BROKERS: str = Field("kafka:9092", description="Comma-separated brokers")
    KAFKA_CLIENT_ID: str = Field("matchmaking-app", description="Kafka client.id")
    TOPIC_PROFILES_CREATED: str = "profiles.created"
    TOPIC_PROFILES_ENRICHED: str = "profiles.enriched"
    TOPIC_PREFERENCES_UPDATED: str = "preferences.updated"
    TOPIC_FEEDBACK_EVENTS: str = "feedback.events"

    # ---- API / misc ----
    APP_ENV: str = Field("dev", description="dev | staging | prod")
    LOG_LEVEL: str = Field("INFO")
    ALLOW_ORIGINS: Optional[List[str]] = None
    SERVICE_NAME: Optional[str] = None  # each service can override

    # ---- Feature flags (can tune at runtime) ----
    ENABLE_EMBEDDINGS: bool = False
    ENABLE_GEO_FILTER: bool = True
    ENABLE_RECIPROCAL_CHECK: bool = True


# Fetch once per process and import this from other modules:
settings = AppSettings()

if not settings.ALLOW_ORIGINS:
    settings.ALLOW_ORIGINS = ["*"]