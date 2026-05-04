"""Miscellaneous utilities for handling TOML files in the plugin creation process.
"""

import os


def is_directory_empty(directory: str) -> bool:
    """Check if a directory is empty.

    Args:
        directory (str): Directory path to check

    Returns:
        bool: True if the directory is empty, False otherwise
    """
    if not os.path.isdir(directory):
        return True

    for _entry in os.scandir(directory):
        return False

    return True


def clean_markdown_text(text: str) -> str:
    """Clean markdown text.

    Args:
        text (str): String to clean

    Returns:
        str: Cleaned string
    """
    for char in r'\`*_{}[]()#+-.!|>~':
        text = text.replace(char, '\\' + char)
    return text


def make_toml_string(text: str) -> str:
    """Create a TOML string from the given text.

    Args:
        text (str): Text to convert

    Returns:
        str: TOML string
    """
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\b', '\\b')
    text = text.replace('\f', '\\f')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    return text


def make_short_description(description: str) -> str:
    """Create a short description from the given description.

    Args:
        description (str): Description to convert

    Returns:
        str: Short description (maximum 200 characters)
    """
    separator = chr(30)  # Record separator character, unlikely to be in the text
    short_description = description.strip()
    short_description = short_description.replace('\r\n', '\n').replace('\r', '\n')
    short_description = short_description.replace('\n\n', separator)
    short_description = short_description.replace('\n', ' ')
    short_description = short_description.split(separator)[0].strip()
    if len(short_description) > 200:
        short_description = short_description[:197] + '...'
    return short_description


def get_locale_list(base_locale: str | None) -> list[tuple[str, str]]:
    """Get a list of locales for the plugin.

    Args:
        base_locale (str | None): Base language for translations
    Returns:
        list[tuple[str, str]]: List of tuples containing locale code and language name
    """
    sample_locales = [
        ('de', 'German'),
        ('en', 'English'),
        ('fr', 'French'),
    ]

    if not base_locale:
        return sample_locales

    return [(code, name) for code, name in sample_locales if not base_locale.startswith(code)]
