from typing import List


def find_target_languages(source_lang: str) -> List[str]:
    """
    Determine the target languages for translation based on the source language.
    This function implements the translation policy of which languages to translate to
    based on the detected source language.

    Args:
        source_lang: The ISO 639-1 language code of the source language (e.g., 'en', 'ko', 'th')

    Returns:
        A list of ISO 639-1 language codes for the target languages to translate to
    """
    if source_lang == "ko":
        return ["th", "en"]

    if source_lang == "en":
        return ["ko", "th"]

    if source_lang == "th":
        return ["ko", "en"]

    return ["en", "ko"]


def find_national_flag(lang_code: str) -> str:
    """
    Get the Slack emoji for the national flag corresponding to a language code.
    This function maps language codes to appropriate flag emojis for visual identification
    in Slack messages.

    Args:
        lang_code: The ISO 639-1 language code (e.g., 'en', 'ko', 'th')

    Returns:
        The Slack emoji code for the national flag (e.g., ':flag-us:', ':flag-kr:')
    """
    if lang_code == "ko":
        return ":flag-kr:"

    if lang_code == "en":
        return ":flag-us:"

    if lang_code == "th":
        return ":flag-th:"

    return ":globe_with_meridians:"
