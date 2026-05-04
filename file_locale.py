"""Plugin locale files generation
"""

import os

from .utils import (
    get_locale_list,
    make_short_description,
    make_toml_string,
)

# TEMPLATE = '''"manifest.description" = "{short_description}"
# "manifest.long_description" = "{description}"
# "manifest.name" = "{name}"
# "message.greeting" = "Hello from the plugin!"
# '''


def write_locale(plugin_dir: str, name: str, description: str, base_locale: str | None, plugin_type: str) -> str | None:
    """Write the locale files.

    Args:
        plugin_dir (str): Plugin directory
        name (str): Plugin name
        description (str): Plugin description
        base_locale (str | None): Base language for translations
        plugin_type (str): Type of plugin

    Returns:
        str | None: Error message or None if successful
    """
    if not base_locale:
        return None

    short_description = make_short_description(description)

    locale_dir = os.path.join(plugin_dir, 'locale')
    try:
        os.makedirs(locale_dir, exist_ok=True)
    except OSError as e:
        return f"Error creating 'locale' directory: {e}"

    lines = [
        f'"manifest.description" = "{make_toml_string(short_description)}"',
        f'"manifest.long_description" = "{make_toml_string(description)}"',
        f'"manifest.name" = "{make_toml_string(name)}"',
    ]

    if plugin_type in ('basic', 'metadata'):
        lines.append('"message.greeting" = "Hello from the plugin!"')

    if plugin_type == 'action':
        lines.append('"action.title" = "Plugin action"')
        lines.append('"action.dialog.title" = "Plugin action"')
        lines.append('"action.dialog.text" = "Action triggered"')

    content = '\n'.join(lines) + '\n'
    locales = [code for code, _ in get_locale_list(base_locale)]
    locales.append(base_locale)
    for loc in locales:
        loc_file = f"{loc}.toml"
        try:
            with open(os.path.join(locale_dir, loc_file), 'w', encoding='utf8') as f:
                f.write(content)
        except OSError as e:
            return f"Error writing 'locale/{loc_file}': {e}"

    return None
