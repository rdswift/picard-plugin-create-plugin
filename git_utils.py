"""Git utility functions for the Create Plugin plugin.
"""

from picard.git.factory import git_backend


def initialize_git_repo(plugin_dir: str, name: str, email: str, initial_commit: bool) -> str | None:
    """Initialize a Git repository in the plugin directory.

    Args:
        plugin_dir (str): Plugin directory
        name (str): User's name
        email (str): User's email
        initial_commit (bool): Whether to make an initial commit
    Returns:
        str | None: Error message or None if successful
    """

    try:
        backend = git_backend()
        repo = backend.init_repository(plugin_dir)

        if initial_commit:
            try:
                backend.add_and_commit_files(
                    repo,
                    'Initial plugin framework',
                    author_name=name,
                    author_email=email,
                )
            finally:
                repo.free()

    except Exception as e:
        return f"Error initializing Git repository: {e}"

    return None
