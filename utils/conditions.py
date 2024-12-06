USER_SEARCH_REQUESTS_SPECIAL_CHARACTERS_ALLOWED = [
    " ",
    "-",
    "—",
    ".",
    "_",
    ":",
]  # спецсимволы разрешенные для использования
# пользователю в поисковых запросах


def is_character_non_special(character: str) -> bool:
    """Проверяет, относится ли символ к специальным символам"""
    return character.isalnum() or character in USER_SEARCH_REQUESTS_SPECIAL_CHARACTERS_ALLOWED
