"""Plugin .gitignore file generation
"""

import os


TEMPLATE_I18N = '''"""Basic Picard 3 plugin with translation support."""

from picard.plugin3.api import (
    PluginApi,
    t_,
)

# Module-level translatable strings (resolved at runtime via api.tr)
GREETING = t_("message.greeting", "Hello from the plugin!")


def enable(api: PluginApi) -> None:
    """Called when the plugin is enabled.

    Use api to register plugin hooks and access essential Picard APIs.
    """
    # Translate a string at runtime
    greeting = api.tr(GREETING, "Hello from the plugin!")
    api.logger.info(greeting)


def disable() -> None:
    """Called when the plugin is disabled."""
'''

TEMPLATE = '''"""Basic Picard 3 plugin."""

from picard.plugin3.api import PluginApi


def enable(api: PluginApi) -> None:
    """Called when the plugin is enabled.

    Use api to register plugin hooks and access essential Picard APIs.
    """
    greeting = "Hello from the plugin!"
    api.logger.info(greeting)


def disable() -> None:
    """Called when the plugin is disabled."""
'''


def write_init(plugin_dir: str, name: str, locale: str | None) -> str | None:
    """Write the __init__.py file.

    Args:
        plugin_dir (str): Plugin directory
        name (str): Plugin name
        locale (str | None): Base locale for translation

    Returns:
        str | None: Error message or None if successful
    """
    content = TEMPLATE_I18N if locale else TEMPLATE
    try:
        with open(os.path.join(plugin_dir, '__init__.py'), 'w', encoding='utf8') as f:
            f.write(content)
    except OSError as e:
        return f"Error writing '__init__.py': {e}"

    return None
