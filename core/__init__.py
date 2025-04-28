"""
Core package for the Slack translation bot.
Contains abstract base classes and data models that form the foundation of the translation system.
"""

from core.db import Database
from core.llm import TranslationRequest, TranslationResponse, LargeLanguageModel

__all__ = [
    "TranslationRequest",
    "TranslationResponse",
    "LargeLanguageModel",
    "Database",
]
