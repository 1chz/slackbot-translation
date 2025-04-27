"""
SQLite database implementation for the Slack translation bot.
"""

import sqlite3
from typing import Optional, Tuple

from core.models.providers import Database

__DB_PATH = "translation.db"


def initialize() -> None:
    """
    Initialize the SQLite database by creating the necessary tables if they don't exist.
    """
    with sqlite3.connect(__DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS message_map (
                src_channel TEXT NOT NULL,
                src_ts      TEXT NOT NULL,
                dst_channel TEXT NOT NULL,
                dst_ts      TEXT NOT NULL,
                PRIMARY KEY (src_channel, src_ts)
            )
        """
        )
        conn.commit()


class SQLiteDatabase(Database):
    """
    SQLite implementation of the Database interface.
    """

    def get_translated_message_reference(
        self, src_channel: str, src_ts: str
    ) -> tuple[str, str]:
        """
        Get the reference to a translated message.

        Args:
            src_channel: The source channel ID
            src_ts: The source message timestamp

        Returns:
            A tuple containing the destination channel ID and message timestamp,
            or None if no reference is found
        """
        with sqlite3.connect("translation.db") as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                "SELECT dst_channel, dst_ts FROM message_map WHERE src_channel = ? AND src_ts = ?",
                (src_channel, src_ts),
            )
            row: Optional[Tuple[str, str]] = cursor.fetchone()
            return row if row else None

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
        with sqlite3.connect("translation.db") as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO message_map (src_channel, src_ts, dst_channel, dst_ts) VALUES (?, ?, ?, ?)",
                (src_channel, src_ts, dst_channel, dst_ts),
            )
            conn.commit()

    def delete_translated_message_reference(
        self, src_channel: str, src_ts: str
    ) -> None:
        """
        Delete a reference to a translated message.

        Args:
            src_channel: The source channel ID
            src_ts: The source message timestamp
        """
        with sqlite3.connect("translation.db") as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM message_map WHERE src_channel = ? AND src_ts = ?",
                (src_channel, src_ts),
            )
            conn.commit()
