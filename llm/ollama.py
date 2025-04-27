"""
Ollama language model provider implementation.
"""

import asyncio

from typing import Dict, List, Any

import requests

from core.models.providers import LargeLanguageModel
from core.models.translation import TranslationRequest, TranslationResponse
from core.utils.language import find_national_flag
from llm.prompts.translation import PROMPT_DETECT_LANGUAGE, PROMPT_TRANSLATE


class OllamaLargeLanguageModel(LargeLanguageModel):
    """
    Ollama implementation of the LanguageModelProvider interface.
    Uses the Ollama API to detect languages and translate text.
    """

    def __init__(self, host: str, model_name: str):
        """
        Initialize the Ollama language model provider.

        Args:
            host: The URL of the Ollama API
            model_name: The name of the Ollama model to use

        Raises:
            ValueError: If host or model_name is None
        """
        if host is None:
            raise ValueError("Ollama host is not set")
        if model_name is None:
            raise ValueError("Ollama model name is not set")

        self.api: str = host
        self.model_name: str = model_name

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to detect the language of

        Returns:
            The ISO 639-1 language code of the detected language
        """
        return self.__query_ollama(PROMPT_DETECT_LANGUAGE, text)

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text from one language to multiple target languages.

        Args:
            request: The translation request containing the text, source language, and target languages

        Returns:
            The translation response containing the translated text in multiple languages
        """

        flag: str = find_national_flag(request.source_lang)
        original_text = f"{flag} {request.text}"

        async def translate_all_async():
            async def _translate_one(target_lang: str) -> str:
                flag: str = find_national_flag(target_lang)
                prompt_with_langs: str = f"""{PROMPT_TRANSLATE}
                        Translate the following text from {request.source_lang} to {target_lang}:"""

                def sync_translate():
                    translated_text: str = self.__query_ollama(
                        prompt_with_langs, request.text
                    )
                    return f"{flag} {translated_text}"

                return await asyncio.to_thread(sync_translate)

            tasks = [_translate_one(lang) for lang in request.target_lang]
            return await asyncio.gather(*tasks)

        translated_texts: List[str] = asyncio.run(translate_all_async())

        return TranslationResponse(
            original_text=original_text, translated_text=translated_texts
        )

    def __query_ollama(self, prompt: str, user_input: str) -> str:
        """
        Query the Ollama API with a prompt and user input.

        Args:
            prompt: The prompt to send to the Ollama API
            user_input: The user input to send to the Ollama API

        Returns:
            The response from the Ollama API

        Raises:
            Exception: If the Ollama API returns an error
        """
        url: str = f"{self.api}/api/generate"
        data: Dict[str, Any] = {
            "model": self.model_name,
            "prompt": f"{prompt}\n\n{user_input}",
            "stream": False,
        }

        response: requests.Response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to query Ollama: {response.text}")

        return response.json()["response"].strip()
