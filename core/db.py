from abc import ABC, abstractmethod
from typing import Tuple


class Database(ABC):
    """
    Abstract base class for database operations.
    Implementations should provide methods for managing translated message references.
    This allows the system to track relationships between original messages and their translations.
    """

    @abstractmethod
    def select_message_map(self, src_channel: str, src_ts: str) -> Tuple[str, str]:
        """
        Retrieves the destination channel and timestamp for a translated message.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message

        Returns:
            A tuple containing the destination channel ID and message timestamp of the translation
        """
        pass

    @abstractmethod
    def insert_message_map(
        self, src_channel: str, src_ts: str, dst_channel: str, dst_ts: str
    ) -> None:
        """
        Stores a mapping between an original message and its translation.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message
            dst_channel: The destination channel ID where the translation was posted
            dst_ts: The destination message timestamp that uniquely identifies the translation
        """
        pass

    @abstractmethod
    def delete_message_map(self, src_channel: str, src_ts: str) -> None:
        """
        Removes a mapping between an original message and its translation.
        This is typically called when a message is deleted.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message
        """
        pass
