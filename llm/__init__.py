"""
Language model package for the Slack translation bot.
Contains language model provider implementations.
"""

from llm.ollama import OllamaLargeLanguageModel
from llm.openai import OpenAILargeLanguageModel

__all__ = [
    "OllamaLargeLanguageModel",
    "OpenAILargeLanguageModel",
]
