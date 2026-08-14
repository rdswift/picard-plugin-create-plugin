"""Plugin locale files generation
"""
# Copyright (C) 2026 Bob Swift (rdswift)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.

from picard.plugin3.init_templates import toml_escape


def generate_locale(name: str, short_description: str, description: str, plugin_types: list[str]) -> str:
    """Generate the content for the locale toml file.

    Args:
        name (str): Plugin name
        short_description (str): Plugin short description
        description (str): Plugin description
        plugin_types (list[str]): Selected plugin code types to include

    Returns:
        str: Content for the locale toml file
    """
    lines = [
        f'"manifest.description" = "{toml_escape(short_description)}"',
        f'"manifest.long_description" = "{toml_escape(description)}"',
        f'"manifest.name" = "{toml_escape(name)}"',
    ]

    if not plugin_types or 'metadata' in plugin_types:
        lines.append('"message.greeting" = "Hello from the plugin!"')

    if 'action' in plugin_types:
        lines.append('"action.title" = "Plugin action"')
        lines.append('"action.dialog.title" = "Plugin action"')
        lines.append('"action.dialog.text" = "Action triggered"')

    if 'options' in plugin_types:
        lines.append('"opt.title.run_image_processor" = "Run image processor"')
        lines.append(
            '"qt.PlaygroundOptionsPage.label.disclaimer" = "This is not a real plugin. It only exists to try the implementation of as much of Picard\'s '
            'plugin API as possible."'
        )
        lines.append('"qt.PlaygroundOptionsPage.label.run_image_processor" = "Run image processor. This applies a sepia effect on all loaded cover images."')
        lines.append('"qt.PlaygroundOptionsPage.title.playground_options" = "API Playground options"')

    return '\n'.join(lines) + '\n'
