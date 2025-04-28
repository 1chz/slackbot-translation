"""
Large Language Model package for the Slack translation bot.
Contains implementations of language model providers for language detection and text translation.
"""

from llm.ollama import OllamaLargeLanguageModel
from llm.openai import OpenAILargeLanguageModel
from llm.prompt import PROMPT_DETECT_LANGUAGE, PROMPT_TRANSLATE

__all__ = [
    "OllamaLargeLanguageModel",
    "OpenAILargeLanguageModel",
]
