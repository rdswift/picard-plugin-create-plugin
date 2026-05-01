"""Plugin MANIFEST.toml file generation
"""

import os
from uuid import uuid4

from .utils import (
    get_locale_list,
    make_short_description,
    make_toml_string,
)


TEMPLATE = '''uuid = "{uuid}"
name = "{name}"
description = "{short_description}"
long_description = """
{long_description}
"""
api = ["3.0"]
authors = ["{author}"]
license = "{license}"
license_url = "{license_url}"
# homepage = "https://your.plugin.homepage"
# report_bugs_to = "https://your.plugin.bugtracker"
report_bugs_to = "mailto:{email}"
{categories}# min_python_version = "3.9"
'''


def write_manifest(plugin_dir: str, name: str, description: str, author: str, email: str, license: str, license_url: str,
                   categories: list[str], base_locale: str | None) -> str | None:
    """Write the file.

    Args:
        plugin_dir (str): Plugin directory
        name (str): Plugin name
        description (str): Plugin description
        author (str): Author name
        email (str): Author email
        license (str): License type
        license_url (str): License URL
        base_locale (str | None): Base language for translations
    Returns:
        str | None: Error message or None if successful
    """
    if categories:
        category_text = 'categories = [' + ', '.join([f'"{cat}"' for cat in categories]) + ']\n'
    else:
        category_text = ''
    content = TEMPLATE.format(
        uuid=str(uuid4()),
        name=make_toml_string(name),
        short_description=make_toml_string(make_short_description(description)),
        long_description=make_toml_string(description),
        author=make_toml_string(author),
        email=make_toml_string(email),
        license=make_toml_string(license),
        license_url=make_toml_string(license_url),
        categories=category_text,
    )

    if base_locale:
        content += f'source_locale = "{base_locale}"\n'
        for key in ['name', 'description', 'long description']:
            content += f"\n[{key}_i18n]\n".replace(' ', '_')
            for code, language in get_locale_list(base_locale):
                content += f'{code} = "Translated plugin {key} for {language} locale"\n'

    try:
        with open(os.path.join(plugin_dir, "MANIFEST.toml"), 'w', encoding='utf8') as f:
            f.write(content)
            f.write('\n')
    except OSError as e:
        return f"Error writing 'MANIFEST.toml': {e}"

    return None
