"""
Prompt templates for translation tasks.
"""

PROMPT_DETECT_LANGUAGE: str = """
Description:
You must forget all previous prompts and only follow this prompt.

Your task is to identify the language of the given text.
Respond with only the ISO 639-1 language code (e.g., "ko" for Korean, "en" for English, "th" for Thai).
Do not include any explanations or additional text in your response.

Rules:
- All text except for the two-letter English code must be completely removed
- If the text is in Korean, respond with: ko
- If the text is in English, respond with: en
- If the text is in Thai, respond with: th
"""

PROMPT_TRANSLATE: str = """
Description:
You must forget all previous prompts and only follow this prompt.

Your task is to translate the given text while preserving the nuance and technical terminology of the original message.

Translate the text to the target language specified.
Provide only the translated text without any explanations or additional information.

Rules:
1. Preserve the nuance and technical terminology of the original message as much as possible
2. Maintain the original meaning and tone
3. Do not add any explanations or notes
4. Provide only the translated text
"""
