"""Miscellaneous utilities for the plugin creation process.
"""


def unwrap_markdown(text: str) -> str:
    """Remove manual line wrapping by replacing line breaks with spaces,
    while preserving paragraph breaks.

    Args:
        text (str): Text to process

    Returns:
        str: Text with manual wrapping removed
    """
    separator = chr(30)  # Record separator character, unlikely to be in the text
    text = text.replace('\r\n', '\n').replace('\r', '\n')   # normalize line breaks to \n
    text = text.replace('\n\n', separator)  # replace multiple newlines with separator
    text = text.replace('\n', ' ')  # replace single newlines with spaces
    text = text.replace(separator, '\n\n')  # return original paragraph breaks
    return text


def make_short_description(description: str) -> str:
    """Create a short description from the given description. The short description is the first
    paragraph of the description, truncated to 200 characters if necessary.

    Args:
        description (str): Description to convert

    Returns:
        str: Short description (maximum 200 characters)
    """
    # unwrap description, extract first paragraph and trim whitespace
    short_description = unwrap_markdown(description).split('\n')[0].strip()

    if len(short_description) > 200:
        short_description = short_description[:197].strip() + '...'

    return short_description
