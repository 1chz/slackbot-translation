# Slack Translation Bot

A Slack bot that automatically translates messages in real-time. The bot detects the language of incoming messages and
translates them to appropriate target languages, posting the translations as threaded replies.

This project follows clean code principles with well-documented interfaces, proper encapsulation of implementation
details,
and clear separation of concerns.

## What This Project Does

This project is a Slack bot that:

- Monitors Slack channels for new messages
- Automatically detects the language of each message
- Translates messages to appropriate target languages
- Posts translations as threaded replies to the original message
- Handles message edits and deletions, updating or removing translations accordingly

## How to Run the Project

### Prerequisites

- Python 3.9+
- A Slack workspace with bot permissions
- API keys for your chosen LLM provider (OpenAI or Ollama)

### Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with the following variables:
   ```
   # Required
   SLACK_APP_TOKEN=xapp-...
   SLACK_BOT_TOKEN=xoxb-...
   LLM_PROVIDER=openai  # or ollama

   # For OpenAI
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-3.5-turbo

   # For Ollama
   OLLAMA_MODEL=llama2

   # Optional
   DB_TYPE=sqlite  # default
   ```

3. Run the bot:
   ```
   python main.py
   ```

## Project Structure

The project is organized into several modules with clear separation of concerns:

- `core/`: Core components, interfaces, and utilities
    - `config.py`: Configuration loading from environment variables
    - `db.py`: Abstract base class for database providers with well-defined interface
    - `llm.py`: Abstract base class for LLM providers and data models for translation
    - `util.py`: Utility functions for language detection and flag emoji mapping

- `db/`: Database implementations
    - `sqlite.py`: SQLite database implementation of the Database interface

- `llm/`: Large Language Model implementations
    - `openai.py`: OpenAI implementation of the LargeLanguageModel interface
    - `ollama.py`: Ollama implementation of the LargeLanguageModel interface
    - `prompt.py`: Internal prompt templates used by LLM implementations

- `middleware/`: Slack event handling middleware
    - `slack_event_handler.py`: Slack event handlers for messages, edits, and deletions

- `factory.py`: Factory for creating LLM and DB instances based on configuration
- `main.py`: Main entry point for the application

## How to Add a New LLM Implementation

To add a new LLM provider:

1. Create a new file in the `llm/` directory (e.g., `llm/my_provider.py`)
2. Implement a class that inherits from `LargeLanguageModel` in `core/llm.py`
3. Implement the required methods:
    - `detect_language(text)`: Detects the language of the given text
    - `translate(request)`: Translates text from one language to multiple target languages
4. Add your implementation to the `__LLM_PROVIDERS` dictionary in `factory.py`

Example:

```python
# llm/my_provider.py
"""
My Provider language model implementation.
"""

from typing import List

from core.llm import LargeLanguageModel, TranslationRequest, TranslationResponse
from core.util import find_national_flag


class MyProviderLargeLanguageModel(LargeLanguageModel):
    """
    My Provider implementation of the LargeLanguageModel interface.
    Uses the My Provider API to detect languages and translate text.
    """

    def __init__(self, api_key: str, model_name: str):
        """
        Initialize the My Provider language model.

        Args:
            api_key: The API key for My Provider
            model_name: The name of the model to use

        Raises:
            ValueError: If api_key or model_name is None
        """
        if api_key is None:
            raise ValueError("My Provider API key is not set")
        if model_name is None:
            raise ValueError("My Provider model name is not set")

        self.__api_key = api_key
        self.__model_name = model_name
        # Initialize your provider's client here

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using My Provider API.

        Args:
            text: The text to detect the language of, can be in any language

        Returns:
            The ISO 639-1 language code of the detected language (e.g., 'en', 'ko', 'th')
        """
        # Implement language detection
        # Return ISO 639-1 language code
        pass

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text from one language to multiple target languages using My Provider API.

        Args:
            request: The translation request containing the text, source language, and target languages

        Returns:
            The translation response containing the original text and translated texts with language flags
        """
        flag: str = find_national_flag(request.source_lang)
        original_text: str = f"{flag} {request.text}"

        # Implement translation for each target language
        translated_texts: List[str] = []
        for target_lang in request.target_lang:
            # Translate text to target language
            translated_text = "Translated text"  # Replace with actual translation
            translated_texts.append(f"{find_national_flag(target_lang)} {translated_text}")

        return TranslationResponse(
            original_text=original_text,
            translated_text=translated_texts
        )


# In factory.py, add:
from llm.my_provider import MyProviderLargeLanguageModel

__LLM_PROVIDERS = {
    # Existing providers...
    "my_provider": MyProviderLargeLanguageModel(
        api_key=config.MY_PROVIDER_API_KEY,
        model_name=config.MY_PROVIDER_MODEL,
    ),
}
```

5. Update `core/config.py` to handle your provider's configuration

## How to Add a New DB Implementation

To add a new database implementation:

1. Create a new file in the `db/` directory (e.g., `db/my_database.py`)
2. Implement a class that inherits from `Database` in `core/models/providers.py`
3. Implement the required methods:
    - `get_translated_message_reference(src_channel, src_ts)`: Gets the reference to a translated message
    - `save_translated_message_reference(src_channel, src_ts, dst_channel, dst_ts)`: Saves a reference to a translated
      message
    - `delete_translated_message_reference(src_channel, src_ts)`: Deletes a reference to a translated message
4. Add your implementation to the `__DATABASES` dictionary in `factory.py`

Example:

```python
# db/my_database.py
"""
My Database implementation for the Slack translation bot.
"""

from typing import Tuple

from core.db import Database


class MyDatabase(Database):
    """
    My Database implementation of the Database interface.
    Provides persistent storage for message mappings using a custom database solution.
    """

    def __init__(self) -> None:
        """
        Initialize the database connection and create necessary tables if they don't exist.
        """
        # Initialize your database connection here
        self.__connection = None  # Replace with actual connection

        # Create tables if they don't exist
        self.__create_tables()

    def __create_tables(self) -> None:
        """
        Create the necessary tables for storing message mappings.
        """
        # Implement table creation logic
        pass

    def select_message_map(self, src_channel: str, src_ts: str) -> Tuple[str, str]:
        """
        Get the reference to a translated message from the database.
        Retrieves the destination channel and timestamp for a message that has been translated.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message

        Returns:
            A tuple containing the destination channel ID and message timestamp of the translation,
            or None if no reference is found for the given source message
        """
        # Implement getting a translation reference
        pass

    def insert_message_map(self, src_channel: str, src_ts: str, dst_channel: str, dst_ts: str) -> None:
        """
        Save a reference to a translated message in the database.
        Creates or updates a mapping between an original message and its translation.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message
            dst_channel: The destination channel ID where the translation was posted
            dst_ts: The destination message timestamp that uniquely identifies the translation
        """
        # Implement saving a translation reference
        pass

    def delete_message_map(self, src_channel: str, src_ts: str) -> None:
        """
        Delete a reference to a translated message from the database.
        Removes the mapping between an original message and its translation.
        This is typically called when a message is deleted in Slack.

        Args:
            src_channel: The source channel ID where the original message was posted
            src_ts: The source message timestamp that uniquely identifies the original message
        """
        # Implement deleting a translation reference
        pass


# In factory.py, add:
from db.my_database import MyDatabase

__DATABASES = {
    # Existing databases...
    "my_database": MyDatabase(),
}
```

5. Update `config.py` to handle your database's configuration
6. Implement an initialization function if needed and update `db/__init__.py`
