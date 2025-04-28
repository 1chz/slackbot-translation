"""
Database package for the Slack translation bot.
Contains database implementations for storing message references between original messages and their translations.
"""

from db.sqlite import SQLiteDatabase

__all__ = [
    "SQLiteDatabase",
]
