"""
Factory module for creating instances of language model providers and databases.
"""

from typing import Dict, Optional

import config
from core.models.providers import Database, LargeLanguageModel
from db import SQLiteDatabase
from llm import OllamaLargeLanguageModel, OpenAILargeLanguageModel

__LLM_PROVIDERS: Dict[str, LargeLanguageModel] = {
    "ollama": OllamaLargeLanguageModel(
        host="http://localhost:11434",
        model_name=config.OLLAMA_MODEL,
    ),
    "openai": OpenAILargeLanguageModel(
        api_key=config.OPENAI_API_KEY,
        model_name=config.OPENAI_MODEL,
    ),
}

__DATABASES: Dict[str, Database] = {
    "sqlite": SQLiteDatabase(),
}


def large_language_model() -> LargeLanguageModel:
    """
    Get the configured language model provider.

    Returns:
        The configured language model provider

    Raises:
        ValueError: If the configured language model provider is not supported
    """
    provider: Optional[LargeLanguageModel] = __LLM_PROVIDERS.get(
        config.LLM_PROVIDER, None
    )
    if provider is None:
        raise ValueError(f"Unsupported language model provider: {config.LLM_PROVIDER}")
    return provider


def database() -> Database:
    """
    Get the configured database.

    Returns:
        The configured database

    Raises:
        ValueError: If the configured database is not supported
    """
    db: Optional[Database] = __DATABASES.get(config.DB_TYPE, None)
    if db is None:
        raise ValueError(f"Unsupported database: {config.DB_TYPE}")
    return db
