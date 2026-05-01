"""Plugin README.md file generation
"""

import os


TEMPLATE = """# {name}

{description}

---

See MANIFEST.toml for plugin license information.
"""


def write_readme(plugin_dir: str, name: str, description: str) -> str | None:
    """Write the file.

    Args:
        plugin_dir (str): Plugin directory
        name (str): Plugin name
        description (str): Plugin description

    Returns:
        str | None: Error message or None if successful
    """
    content = TEMPLATE.format(name=name, description=description)
    try:
        with open(os.path.join(plugin_dir, 'README.md'), 'w', encoding='utf8') as f:
            f.write(content)
    except OSError as e:
        return f"Error writing 'README.md': {e}"

    return None
