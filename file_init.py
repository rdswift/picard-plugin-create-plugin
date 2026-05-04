"""Plugin __init__.py file generation
"""
# Code examples for the __init__.py file are based on the playgound / testing plugin by Philipp Wolfer.
# See https://git.sr.ht/~phw/picard-plugin-playground

from collections import OrderedDict
import os

from picard.plugin3.api import t_


def _basic_template(i18n_support: bool = False) -> str:
    """Get the basic __init__.py template.

    Args:
        i18n_support (bool): Whether to include translation support in the template

    Returns:
        str: The basic __init__.py template
    """
    if i18n_support:
        lines = [
            '"""Basic Picard 3 plugin with translation support."""',
            '',
            'from picard.plugin3.api import (',
            '    PluginApi,',
            '    t_,',
            ')',
            '',
            '# Module-level translatable strings (resolved at runtime via api.tr)',
            'GREETING = t_("message.greeting", "Hello from the plugin!")',
        ]
    else:
        lines = [
            '"""Basic Picard 3 plugin."""',
            '',
            'from picard.plugin3.api import PluginApi',
        ]
    lines.append('')
    lines.append('')
    lines.append('def enable(api: PluginApi) -> None:')
    lines.append('    """Called when the plugin is enabled.')
    lines.append('')
    lines.append('    Use api to register plugin hooks and access essential Picard APIs.')
    lines.append('    """')
    if i18n_support:
        lines.append('    # Translate a string at runtime')
        lines.append('    greeting = api.tr(GREETING, "Hello from the plugin!")')
    else:
        lines.append('    greeting = "Hello from the plugin!"')
    lines.append('    api.logger.info(greeting)')
    lines.append('')
    lines.append('')
    lines.append('def disable() -> None:')
    lines.append('    """Called when the plugin is disabled."""')
    lines.append('    pass')
    return '\n'.join(lines)


def _metadata_template(i18n_support: bool = False) -> str:
    """Get the metadata processing __init__.py template.

    Args:
        i18n_support (bool): Whether to include translation support in the template

    Returns:
        str: The metadata processing __init__.py template
    """
    if i18n_support:
        lines = [
            '"""Picard 3 metadata plugin with translation support."""',
        ]
    else:
        lines = [
            '"""Picard 3 metadata plugin."""',
        ]
    lines.append('')
    lines.append('from picard.plugin3.api import (')
    lines.append('    Album,')
    lines.append('    Metadata,')
    lines.append('    PluginApi,')
    lines.append('    Track,')
    if i18n_support:
        lines.append('    t_,')
    lines.append(')')
    if i18n_support:
        lines.append('')
        lines.append('')
        lines.append('# Module-level translatable strings (resolved at runtime via api.tr)')
        lines.append('GREETING = t_("message.greeting", "Hello from the plugin!")')
    lines.append('')
    lines.append('')
    lines.append('def album_metadata_processor(')
    lines.append('    api: PluginApi,')
    lines.append('    album: Album,')
    lines.append('    metadata: Metadata,')
    lines.append('    release_node: dict,')
    lines.append('):')
    lines.append('    logger = api.logger')
    lines.append('    logger.info("Album metadata processor called:")')
    lines.append('    logger.info(f"album: {album}")')
    lines.append('    logger.info(f"metadata: {metadata}")')
    lines.append('    logger.info(f"release_node: {release_node}")')
    lines.append('')
    lines.append('')
    lines.append('def track_metadata_processor(')
    lines.append('    api: PluginApi,')
    lines.append('    track: Track,')
    lines.append('    metadata: Metadata,')
    lines.append('    track_node: dict,')
    lines.append('    release_node: dict | None,')
    lines.append('):')
    lines.append('    logger = api.logger')
    lines.append('    logger.info("Track metadata processor called:")')
    lines.append('    logger.info(f"track: {track}")')
    lines.append('    logger.info(f"metadata: {metadata}")')
    lines.append('    logger.info(f"track_node: {track_node}")')
    lines.append('    logger.info(f"release_node: {release_node}")')
    lines.append('')
    lines.append('')
    lines.append('def enable(api: PluginApi) -> None:')
    lines.append('    """Called when the plugin is enabled.')
    lines.append('')
    lines.append('    Use api to register plugin hooks and access essential Picard APIs.')
    lines.append('    """')
    if i18n_support:
        lines.append('    # Translate a string at runtime')
        lines.append('    greeting = api.tr(GREETING, "Hello from the plugin!")')
        lines.append('    api.logger.info(greeting)')
        lines.append('')
    lines.append('    # Metadata processors')
    lines.append('    api.register_album_metadata_processor(album_metadata_processor)')
    lines.append('    api.register_track_metadata_processor(track_metadata_processor)')
    lines.append('')
    lines.append('')
    lines.append('def disable() -> None:')
    lines.append('    """Called when the plugin is disabled."""')
    lines.append('    pass')
    return '\n'.join(lines)


def _action_template(i18n_support: bool = False) -> str:
    """Get the action plugin __init__.py template.

    Args:
        i18n_support (bool): Whether to include translation support in the template

    Returns:
        str: The action plugin __init__.py template
    """
    if i18n_support:
        lines = [
            '"""Picard 3 menu action plugin with translation support."""',
        ]
    else:
        lines = [
            '"""Picard 3 menu action plugin."""',
        ]
    lines.append('')
    lines.append('from picard.plugin3.api import (')
    lines.append('    BaseAction,')
    lines.append('    PluginApi,')
    if i18n_support:
        lines.append('    t_,')
    lines.append(')')
    lines.append('')
    lines.append('from PyQt6.QtWidgets import QMessageBox')
    lines.append('')
    lines.append('')
    lines.append('class MyAction(BaseAction):',)
    if i18n_support:
        lines.append('    TITLE = t_("action.title", "Plugin action")')
    else:
        lines.append('    TITLE = "Plugin action"')
    lines.append('')
    lines.append('    def callback(self, objs):')
    lines.append('        self.api.logger.info(f"Action called with {len(objs)} objects")')
    lines.append('        for obj in objs:')
    lines.append('            self.api.logger.info(str(obj))')
    lines.append('')
    lines.append('        QMessageBox.information(')
    lines.append('            None,')
    if i18n_support:
        lines.append('            self.api.tr("action.dialog.title", "Plugin action"),')
        lines.append('            self.api.tr("action.dialog.text", "Action triggered"),')
    else:
        lines.append('            "Plugin action",')
        lines.append('            "Action triggered",')
    lines.append('        )')
    lines.append('')
    lines.append('')
    lines.append('def enable(api: PluginApi) -> None:')
    lines.append('    """Called when the plugin is enabled.')
    lines.append('')
    lines.append('    Use api to register plugin hooks and access essential Picard APIs.')
    lines.append('    """')
    lines.append('    # Actions')
    lines.append('    api.register_album_action(MyAction)')
    lines.append('    api.register_cluster_action(MyAction)')
    lines.append('    api.register_clusterlist_action(MyAction)')
    lines.append('    api.register_file_action(MyAction)')
    lines.append('    api.register_track_action(MyAction)')
    lines.append('    api.register_tools_menu_action(MyAction)')
    lines.append('')
    lines.append('')
    lines.append('def disable() -> None:')
    lines.append('    """Called when the plugin is disabled."""')
    lines.append('    pass')
    return '\n'.join(lines)


CODE_TEMPLATES = OrderedDict(
    [
        ('basic', {
            'name': t_("code_example.basic", "Basic plugin"),
            'code_generator': _basic_template,
        }),
        ('metadata', {
            'name': t_("code_example.metadata", "Metadata plugin"),
            'code_generator': _metadata_template,
        }),
        ('action', {
            'name': t_("code_example.action", "Menu action plugin"),
            'code_generator': _action_template,
        }),
    ]
)


def write_init(plugin_dir: str, template: str, i18n_support: bool = False) -> str | None:
    """Write the __init__.py file.

    Args:
        plugin_dir (str): Plugin directory
        template (str): Template to use
        i18n_support (bool): Whether to include translation support in the template

    Returns:
        str | None: Error message or None if successful
    """
    if template not in CODE_TEMPLATES:
        return f"Template '{template}' not found"

    code_generator = CODE_TEMPLATES[template]['code_generator']
    content = code_generator(i18n_support=i18n_support) + '\n'
    try:
        with open(os.path.join(plugin_dir, '__init__.py'), 'w', encoding='utf8') as f:
            f.write(content)
    except OSError as e:
        return f"Error writing '__init__.py': {e}"

    return None
