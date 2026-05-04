"""Plugin .gitignore file generation
"""

import os


TEMPLATE = """# Plugin: {name}
.project
picard
*.orig
*.bak
__pycache__/
*.py[cod]
*.egg-info/
dist/
"""


def write_gitignore(plugin_dir: str, name: str) -> str | None:
    """Write the .gitignore file.

    Args:
        plugin_dir (str): Plugin directory
        name (str): Plugin name

    Returns:
        str | None: Error message or None if successful
    """
    content = TEMPLATE.format(name=name)
    try:
        with open(os.path.join(plugin_dir, '.gitignore'), 'w', encoding='utf8') as f:
            f.write(content)
    except OSError as e:
        return f"Error writing '.gitignore': {e}"

    return None
