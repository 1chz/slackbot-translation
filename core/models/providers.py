from abc import ABC, abstractmethod
from typing import Tuple

from core.models.translation import TranslationRequest, TranslationResponse


class LargeLanguageModel(ABC):
    """
    Abstract base class for language model providers.
    Implementations should provide methods for language detection and translation.
    """

    @abstractmethod
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to detect the language of

        Returns:
            The ISO 639-1 language code of the detected language
        """
        pass

    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text from one language to multiple target languages.

        Args:
            request: The translation request containing the text, source language, and target languages

        Returns:
            The translation response containing the translated text in multiple languages
        """
        pass


class Database(ABC):
    """
    Abstract base class for database operations.
    Implementations should provide methods for managing translated message references.
    """

    @abstractmethod
    def get_translated_message_reference(
        self, src_channel: str, src_ts: str
    ) -> Tuple[str, str]:
        """
        Get the reference to a translated message.

        Args:
            src_channel: The source channel ID
            src_ts: The source message timestamp

        Returns:
            A tuple containing the destination channel ID and message timestamp
        """
        pass

    @abstractmethod
    def save_translated_message_reference(
        self, src_channel: str, src_ts: str, dst_channel: str, dst_ts: str
    ) -> None:
        """
        Save a reference to a translated message.

        Args:
            src_channel: The source channel ID
            src_ts: The source message timestamp
            dst_channel: The destination channel ID
            dst_ts: The destination message timestamp
        """
        pass

    @abstractmethod
    def delete_translated_message_reference(
        self, src_channel: str, src_ts: str
    ) -> None:
        """
        Delete a reference to a translated message.

        Args:
            src_channel: The source channel ID
            src_ts: The source message timestamp
        """
        pass
