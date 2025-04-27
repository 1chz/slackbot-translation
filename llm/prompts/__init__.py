"""
Prompts package for the Slack translation bot.
Contains prompt templates for language models.
"""

from llm.prompts.translation import PROMPT_DETECT_LANGUAGE, PROMPT_TRANSLATE

__all__ = ["PROMPT_DETECT_LANGUAGE", "PROMPT_TRANSLATE"]
