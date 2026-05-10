"""Plugin .gitignore file generation
"""

import os


TEMPLATE = """# Byte-compiled / optimized / DLL files
*.py[cod]
__pycache__/

# Environments and development tools
.venv/
.ruff_cache/

# Distribution / packaging
*.egg-info/
dist/
"""


# TODO: Use code available in Picard

def write_gitignore(plugin_dir: str) -> str | None:
    """Write the .gitignore file.

    Args:
        plugin_dir (str): Plugin directory

    Returns:
        str | None: Error message or None if successful
    """
    try:
        with open(os.path.join(plugin_dir, '.gitignore'), 'w', encoding='utf8') as f:
            f.write(TEMPLATE)
    except OSError as e:
        return f"Error writing '.gitignore': {e}"

    return None
