from typing import List


def find_target_languages(source_lang: str) -> List[str]:
    """
    Determine the target languages for translation based on the source language.

    Args:
        source_lang: The ISO 639-1 language code of the source language

    Returns:
        A list of ISO 639-1 language codes for the target languages
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

    Args:
        lang_code: The ISO 639-1 language code

    Returns:
        The Slack emoji for the national flag
    """
    if lang_code == "ko":
        return ":flag-kr:"

    if lang_code == "en":
        return ":flag-us:"

    if lang_code == "th":
        return ":flag-th:"

    return ":globe_with_meridians:"
