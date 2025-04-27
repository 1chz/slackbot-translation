# Slack Translation Bot

A Slack bot that automatically translates messages in real-time. The bot detects the language of incoming messages and translates them to appropriate target languages, posting the translations as threaded replies.

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

The project is organized into several modules:

- `core/`: Core models and utilities
  - `models/`: Data models and provider interfaces
    - `providers.py`: Abstract base classes for LLM and DB providers
    - `translation.py`: Translation request and response models
  - `utils/`: Utility functions
    - `language.py`: Language detection and flag utilities

- `db/`: Database implementations
  - `sqlite.py`: SQLite database implementation

- `llm/`: Large Language Model implementations
  - `openai.py`: OpenAI implementation
  - `ollama.py`: Ollama implementation
  - `prompts/`: Prompt templates for LLMs

- `slack/`: Slack bot implementation
  - `bot.py`: Slack event handlers and message formatting

- `config.py`: Configuration loading from environment variables
- `factory.py`: Factory for creating LLM and DB instances
- `main.py`: Main entry point for the application

## How to Add a New LLM Implementation

To add a new LLM provider:

1. Create a new file in the `llm/` directory (e.g., `llm/my_provider.py`)
2. Implement a class that inherits from `LargeLanguageModel` in `core/models/providers.py`
3. Implement the required methods:
   - `detect_language(text)`: Detects the language of the given text
   - `translate(request)`: Translates text from one language to multiple target languages
4. Add your implementation to the `__LLM_PROVIDERS` dictionary in `factory.py`

Example:

```python
# llm/my_provider.py
from core.models.providers import LargeLanguageModel
from core.models.translation import TranslationRequest, TranslationResponse
from core.utils.language import find_national_flag

class MyProviderLargeLanguageModel(LargeLanguageModel):
    def __init__(self, api_key, model_name):
        self.__api_key = api_key
        self.__model_name = model_name
        # Initialize your provider's client here

    def detect_language(self, text: str) -> str:
        # Implement language detection
        # Return ISO 639-1 language code
        pass

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        # Implement translation
        # Return TranslationResponse with translated texts
        pass

# In factory.py, add:
from llm import MyProviderLargeLanguageModel

__LLM_PROVIDERS = {
    # Existing providers...
    "my_provider": MyProviderLargeLanguageModel(
        api_key=config.MY_PROVIDER_API_KEY,
        model_name=config.MY_PROVIDER_MODEL,
    ),
}
```

5. Update `config.py` to handle your provider's configuration

## How to Add a New DB Implementation

To add a new database implementation:

1. Create a new file in the `db/` directory (e.g., `db/my_database.py`)
2. Implement a class that inherits from `Database` in `core/models/providers.py`
3. Implement the required methods:
   - `get_translated_message_reference(src_channel, src_ts)`: Gets the reference to a translated message
   - `save_translated_message_reference(src_channel, src_ts, dst_channel, dst_ts)`: Saves a reference to a translated message
   - `delete_translated_message_reference(src_channel, src_ts)`: Deletes a reference to a translated message
4. Add your implementation to the `__DATABASES` dictionary in `factory.py`

Example:

```python
# db/my_database.py
from core.models.providers import Database

class MyDatabase(Database):
    def __init__(self):
        # Initialize your database connection here
        pass

    def get_translated_message_reference(self, src_channel: str, src_ts: str) -> tuple[str, str]:
        # Implement getting a translation reference
        pass

    def save_translated_message_reference(self, src_channel: str, src_ts: str, dst_channel: str, dst_ts: str) -> None:
        # Implement saving a translation reference
        pass

    def delete_translated_message_reference(self, src_channel: str, src_ts: str) -> None:
        # Implement deleting a translation reference
        pass

# In factory.py, add:
from db import MyDatabase

__DATABASES = {
    # Existing databases...
    "my_database": MyDatabase(),
}
```

5. Update `config.py` to handle your database's configuration
6. Implement an initialization function if needed and update `db/__init__.py`
