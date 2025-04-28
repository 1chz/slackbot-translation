from slack_bolt.adapter.socket_mode import SocketModeHandler

from core import config
from middleware import app


def _main() -> None:
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    _main()
