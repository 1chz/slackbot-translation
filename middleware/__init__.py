"""
Middleware package for the Slack translation bot.
Contains event handling implementation for processing Slack messages, including message creation, editing, and deletion.
"""

from middleware.slack_event_handler import app

__all__ = [
    "app",
]
