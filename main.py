"""
Main entry point for the Slack translation bot.
"""

import config
from db import initialize
from slack import app
from slack_bolt.adapter.socket_mode import SocketModeHandler


def _main() -> None:
    """
    Initialize the database and start the Slack bot.
    """
    initialize()
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    _main()
