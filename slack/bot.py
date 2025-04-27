"""
Slack bot implementation for the translation bot.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Callable

from slack_bolt import App

import config
import factory
from core.models.translation import TranslationRequest, TranslationResponse
from core.utils.language import find_target_languages

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("slack_translation_bot")

app: App = App(token=config.SLACK_BOT_TOKEN)

LARGE_LANGUAGE_MODEL: Any = factory.large_language_model()
DATABASE: Any = factory.database()

SECTION_BLOCK_TYPE = "section"
DIVIDER_BLOCK = {"type": "divider"}


@app.event({"type": "message", "subtype": None})
def handle_new_message(event: Dict[str, Any], say: Callable, client: Any) -> None:
    """
    Handle new messages in Slack.

    Args:
        event: The Slack event
        say: Function to send a message to Slack
    """
    if __is_bot_message(event):
        logger.debug("Ignoring bot message")
        return

    channel: str = event.get("channel")
    ts: str = event.get("ts")
    text: str = event.get("text", "")

    logger.debug(f"Processing new message in channel {channel} with timestamp {ts}")
    response: Optional[Dict[str, Any]] = say(
        channel=channel, thread_ts=ts, text=":hourglass_flowing_sand: Translating..."
    )
    if response:
        logger.debug("Saving translation reference to database")
        DATABASE.save_translated_message_reference(
            src_channel=channel,
            src_ts=ts,
            dst_channel=response["channel"],
            dst_ts=response["ts"],
        )

    source_lang: str = LARGE_LANGUAGE_MODEL.detect_language(text)
    logger.debug(f"Detected language: {source_lang}")

    target_langs: List[str] = find_target_languages(source_lang)
    logger.debug(f"Target languages: {target_langs}")

    translation_request: TranslationRequest = TranslationRequest(
        text=text, source_lang=source_lang, target_lang=target_langs
    )

    logger.debug("Translating message")
    translation_response: TranslationResponse = LARGE_LANGUAGE_MODEL.translate(
        translation_request
    )
    slack_message: Dict[str, Any] = __format_translation_as_slack_message(
        translation_response
    )

    logger.debug("Updating translation as reply")
    client.chat_update(
        channel=response["channel"],
        ts=response["ts"],
        text="Translated message...",
        blocks=slack_message["blocks"],
    )


@app.event({"type": "message", "subtype": "message_changed"})
def handle_message_edit(event: Dict[str, Any], client: Any) -> None:
    """
    Handle edited messages in Slack.

    Args:
        event: The Slack event
        client: The Slack client
    """
    message: Dict[str, Any] = event.get("message", {})

    if __is_bot_message(message):
        logger.debug("Ignoring bot message edit")
        return

    channel: str = event.get("channel")
    ts: str = message.get("ts")
    text: str = message.get("text", "")

    if text == "This message was deleted.":
        logger.debug("top-level thread deleted")
        handle_message_delete(event, client)
        return

    logger.debug(f"Processing edited message in channel {channel} with timestamp {ts}")

    source_lang: str = LARGE_LANGUAGE_MODEL.detect_language(text)
    logger.debug(f"Detected language: {source_lang}")

    target_langs: List[str] = find_target_languages(source_lang)
    logger.debug(f"Target languages: {target_langs}")

    logger.debug("Checking for existing translation")
    translations: Optional[Tuple[str, str]] = DATABASE.get_translated_message_reference(
        channel, ts
    )

    if translations:
        dst_channel: str
        dst_ts: str
        dst_channel, dst_ts = translations
        logger.debug(
            f"Found existing translation in channel {dst_channel} with timestamp {dst_ts}"
        )

        translation_request: TranslationRequest = TranslationRequest(
            text=text, source_lang=source_lang, target_lang=target_langs
        )

        logger.debug("Translating edited message")
        translation_response: TranslationResponse = LARGE_LANGUAGE_MODEL.translate(
            translation_request
        )
        slack_message: Dict[str, Any] = __format_translation_as_slack_message(
            translation_response
        )

        logger.debug("Updating existing translation")
        client.chat_update(
            channel=dst_channel,
            ts=dst_ts,
            text="This is the translated message...",
            blocks=slack_message["blocks"],
        )

    else:
        logger.debug("No existing translation found, handling as new message")
        new_event: Dict[str, Any] = event.copy()
        new_event.update({"channel": channel, "ts": ts, "text": text})

        handle_new_message(
            new_event,
            lambda _text, thread_ts: client.chat_postMessage(
                channel=channel, text=_text, thread_ts=thread_ts
            ),
        )


@app.event({"type": "message", "subtype": "message_deleted"})
def handle_message_delete(event: Dict[str, Any], client: Any) -> None:
    """
    Handle deleted messages in Slack.

    Args:
        event: The Slack event
        client: The Slack client
    """
    if __is_bot_message(event.get("previous_message", {})):
        logger.debug("Ignoring bot message delete")
        return

    channel: str = event.get("channel")
    ts: str = event.get("previous_message", {}).get("ts")

    logger.debug(f"Processing deleted message in channel {channel} with timestamp {ts}")

    logger.debug("Checking for existing translation")
    translations: Optional[Tuple[str, str]] = DATABASE.get_translated_message_reference(
        channel, ts
    )

    if translations:
        dst_channel, dst_ts = translations
        logger.debug(
            f"Found existing translation in channel {dst_channel} with timestamp {dst_ts}"
        )

        logger.debug("Deleting translation")
        client.chat_delete(channel=dst_channel, ts=dst_ts)

        logger.debug("Removing translation reference from database")
        DATABASE.delete_translated_message_reference(channel, ts)


def __is_bot_message(message: Dict[str, Any]) -> bool:
    """
    Check if a message is from a bot.

    Args:
        message: The Slack message

    Returns:
        True if the message is from a bot, False otherwise
    """
    return message.get("subtype") == "bot_message" or message.get("bot_id") is not None


def __format_translation_as_slack_message(
    response: TranslationResponse,
) -> Dict[str, Any]:
    """
    Format the translation response as a Slack message.

    Args:
        response: The translation response object.

    Returns:
        A Slack message structure as a dictionary.
    """
    message_blocks = [
        __section_block(response.original_text),
        DIVIDER_BLOCK,
    ]
    message_blocks.extend(
        __section_block(translated_text) for translated_text in response.translated_text
    )
    return {"blocks": message_blocks}


def __section_block(text: str) -> Dict[str, Any]:
    section_block = {
        "type": SECTION_BLOCK_TYPE,
        "fields": [{"type": "mrkdwn", "text": text}],
    }
    return section_block
