"""
OpenAI language model provider implementation.
"""

import asyncio
from typing import List


from openai import OpenAI

from core.models.providers import LargeLanguageModel
from core.models.translation import TranslationRequest, TranslationResponse
from core.utils.language import find_national_flag
from llm.prompts.translation import PROMPT_DETECT_LANGUAGE, PROMPT_TRANSLATE


class OpenAILargeLanguageModel(LargeLanguageModel):
    """
    OpenAI implementation of the LanguageModelProvider interface.
    Uses the OpenAI API to detect languages and translate text.
    """

    def __init__(self, api_key: str, model_name: str):
        """
        Initialize the OpenAI language model provider.

        Args:
            api_key: The OpenAI API key
            model_name: The name of the OpenAI model to use

        Raises:
            ValueError: If api_key or model_name is None
        """
        if api_key is None:
            raise ValueError("OpenAI API key is not set")
        if model_name is None:
            raise ValueError("OpenAI model name is not set")

        self.__client = OpenAI(api_key=api_key)
        self.__model_name = model_name

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to detect the language of

        Returns:
            The ISO 639-1 language code of the detected language
        """
        response = self.__client.responses.create(
            model=self.__model_name,
            instructions=PROMPT_DETECT_LANGUAGE,
            input=text,
        )
        return response.output_text.strip()

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text from one language to multiple target languages.

        Args:
            request: The translation request containing the text, source language, and target languages

        Returns:
            The translation response containing the translated text in multiple languages
        """

        flag = find_national_flag(request.source_lang)
        original_text = f"{flag} {request.text.strip()}"

        async def translate_all_async():
            async def _translate_one(target_lang):
                flag = find_national_flag(target_lang)

                def sync_translate():
                    response = self.__client.responses.create(
                        model=self.__model_name,
                        instructions=PROMPT_TRANSLATE,
                        input=f"""
                        Translate the following text from {request.source_lang} to {target_lang}:\n{request.text}""",
                    )
                    return f"{flag} {response.output_text.strip()}"

                return await asyncio.to_thread(sync_translate)

            tasks = [_translate_one(lang) for lang in request.target_lang]
            return await asyncio.gather(*tasks)

        translated_texts: List[str] = asyncio.run(translate_all_async())

        return TranslationResponse(
            original_text=original_text, translated_text=translated_texts
        )
