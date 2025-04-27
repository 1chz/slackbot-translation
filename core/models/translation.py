from dataclasses import dataclass
from typing import List


@dataclass
class TranslationRequest:
    """
    Represents a request to translate text from one language to multiple target languages.
    """

    text: str
    source_lang: str
    target_lang: List[str]


@dataclass
class TranslationResponse:
    """
    Represents the response containing translated text in multiple languages.
    """

    original_text: str
    translated_text: List[str]
