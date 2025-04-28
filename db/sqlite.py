"""
SQLite database implementation for the Slack translation core.
"""

import sqlite3
from typing import Optional, Tuple

from core.db import Database

_DB_PATH = "translation.db"


class SQLiteDatabase(Database):
    """
    SQLite implementation of the Database interface.
    Provides persistent storage for message mappings using SQLite database.
    """

    def __init__(self) -> None:
        """
        Initialize the SQLite database by creating the necessary tables if they don't exist.
        Creates a message_map table to store relationships between original messages and translations.
        """
        with sqlite3.connect(_DB_PATH) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                """
                create table if not exists message_map
                (
                    src_channel text not null,
                    src_ts      text not null,
                    dst_channel text not null,
                    dst_ts      text not null,
                    primary key (src_channel, src_ts)
                )
                """
            )
            conn.commit()

    def select_message_map(self, src_channel: str, src_ts: str) -> tuple[str, str]:
        """
        Get the reference to a translated message from the SQLite database.
        Retrieves the destination channel and timestamp for a message that has been translated.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message

        Returns:
            A tuple containing the destination channel ID and message timestamp of the translation,
            or None if no reference is found for the given source message
        """
        with sqlite3.connect(_DB_PATH) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                "select dst_channel, dst_ts from message_map where src_channel = ? and src_ts = ?",
                (src_channel, src_ts),
            )
            row: Optional[Tuple[str, str]] = cursor.fetchone()
            return row if row else None

    def insert_message_map(
        self, src_channel: str, src_ts: str, dst_channel: str, dst_ts: str
    ) -> None:
        """
        Save a reference to a translated message in the SQLite database.
        Creates or updates a mapping between an original message and its translation.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message
            dst_channel: The destination channel ID where the translation was posted
            dst_ts: The destination message timestamp that uniquely identifies the translation
        """
        with sqlite3.connect(_DB_PATH) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                "insert into message_map (src_channel, src_ts, dst_channel, dst_ts) values (?, ?, ?, ?)",
                (src_channel, src_ts, dst_channel, dst_ts),
            )
            conn.commit()

    def delete_message_map(self, src_channel: str, src_ts: str) -> None:
        """
        Delete a reference to a translated message from the SQLite database.
        Removes the mapping between an original message and its translation.
        This is typically called when a message is deleted in Slack.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message
        """
        with sqlite3.connect(_DB_PATH) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                "delete from message_map where src_channel = ? and src_ts = ?",
                (src_channel, src_ts),
            )
            conn.commit()
