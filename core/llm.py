from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import List


@dataclass
class TranslationRequest:
    """
    Represents a request to translate text from one language to multiple target languages.
    This data class encapsulates all the information needed for a translation operation.
    """

    text: str  # The text to be translated
    source_lang: str  # The ISO 639-1 language code of the source language
    target_lang: List[str]  # List of ISO 639-1 language codes for target languages


@dataclass
class TranslationResponse:
    """
    Represents the response containing translated text in multiple languages.
    This data class encapsulates the results of a translation operation.
    """

    original_text: str  # The original text with the language flag prefix
    translated_text: List[str]  # List of translated texts with language flag prefixes


class LargeLanguageModel(ABC):
    """
    Abstract base class for language model providers.
    Implementations should provide methods for language detection and translation.
    This class defines the interface that all language model implementations must follow.
    """

    @abstractmethod
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using the language model.

        Args:
            text: The text to detect the language of, can be in any language

        Returns:
            The ISO 639-1 language code of the detected language (e.g., 'en', 'ko', 'th')
        """
        pass

    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text from one language to multiple target languages.
        Implementations should handle the translation process and formatting of the response.

        Args:
            request: The translation request containing the text, source language, and target languages

        Returns:
            The translation response containing the original text and translated texts with language flags
        """
        pass
