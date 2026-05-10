"""Miscellaneous utilities for the plugin creation process.
"""

import os
import re
import unicodedata


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


# TODO: Use code available in Picard

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


# TODO: Use code available in Picard

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
    """Create a short description from the given description. The short description is the first
    paragraph of the description, truncated to 200 characters if necessary.

    The description is first reformatted to accomodate lines possiblely wrapped manually, by
    replacing line breaks with spaces, while preserving paragraph breaks. Then the first paragraph
    is extracted and truncated if it exceeds 200 characters.

    Args:
        description (str): Description to convert

    Returns:
        str: Short description (maximum 200 characters)
    """
    separator = chr(30)  # Record separator character, unlikely to be in the text

    short_description = description.strip()

    # normalize line breaks to \n
    short_description = short_description.replace('\r\n', '\n').replace('\r', '\n')

    # replace multiple newlines with separator
    short_description = short_description.replace('\n\n', separator)

    # replace single newlines with spaces
    short_description = short_description.replace('\n', ' ')

    # extract first paragraph and trim whitespace
    short_description = short_description.split(separator)[0].strip()

    if len(short_description) > 200:
        short_description = short_description[:197] + '...'

    return short_description


def get_locale_list(base_locale: str | None) -> list[tuple[str, str]]:
    """Get a list of example locales for the plugin, not including the base locale.

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


# TODO: Use code available in Picard

def slugify(value: str):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    value = re.sub(r'[-\s]+', '-', value).strip('-_')
    return value
