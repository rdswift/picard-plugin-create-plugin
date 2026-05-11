"""Plugin __init__.py file generation
"""
# Code examples for the generated __init__.py file are based on the
# playgound / testing plugin by Philipp Wolfer.
#
# See https://git.sr.ht/~phw/picard-plugin-playground

from collections import (
    OrderedDict,
    namedtuple,
)

from picard.plugin3.api import (
    PluginApi,
    t_,
)


Include = namedtuple('Include', ['module', 'name'])


class CodeTemplate:
    i18n_block: str = ''
    registration_block: str = ''
    includes: set[Include] = set()

    def __init__(self) -> None:
        pass

    @classmethod
    def code_block(cls, i18n_support: bool = False) -> str:
        return ''


class CodeMetadata(CodeTemplate):
    registration_block = (
        '\n'
        '    # Metadata processors\n'
        '    api.register_album_metadata_processor(album_metadata_processor)\n'
        '    api.register_track_metadata_processor(track_metadata_processor)\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='Album'),
        Include(module='picard.plugin3.api', name='Metadata'),
        Include(module='picard.plugin3.api', name='Track'),
        Include(module='PyQt6', name='QtCore'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        return (
            '\n\n'
            'def album_metadata_processor(\n'
            '    api: PluginApi,\n'
            '    album: Album,\n'
            '    metadata: Metadata,\n'
            '    release_node: dict,\n'
            '):\n'
            '    logger = api.logger\n'
            '    logger.info("Album metadata processor called:")\n'
            '    logger.info(f"album: {album}")\n'
            '    logger.info(f"metadata: {metadata}")\n'
            '    logger.info(f"release_node: {release_node}")\n'
            '\n'
            "    # Let's fake some work by artificially delaying the request\n"
            '    api.add_album_task(album, "playground_delay", "playground fake task")\n'
            '\n'
            '    def callback() -> None:\n'
            '        logger.info(f"Album task finished for {album}.")\n'
            '\n'
            '    QtCore.QTimer.singleShot(2000, callback)\n'
            '\n\n'
            'def track_metadata_processor(\n'
            '    api: PluginApi,\n'
            '    track: Track,\n'
            '    metadata: Metadata,\n'
            '    track_node: dict,\n'
            '    release_node: dict | None,\n'
            '):\n'
            '    logger = api.logger\n'
            '    logger.info("Track metadata processor called:")\n'
            '    logger.info(f"track: {track}")\n'
            '    logger.info(f"metadata: {metadata}")\n'
            '    logger.info(f"track_node: {track_node}")\n'
            '    logger.info(f"release_node: {release_node}")\n'
        )


class CodeAction(CodeTemplate):
    registration_block = (
        '\n'
        '    # Menu actions\n'
        '    api.register_album_action(MyAction)\n'
        '    api.register_cluster_action(MyAction)\n'
        '    api.register_clusterlist_action(MyAction)\n'
        '    api.register_file_action(MyAction)\n'
        '    api.register_track_action(MyAction)\n'
        '    api.register_tools_menu_action(MyAction)\n'
    )
    includes = {
        Include(module='PyQt6.QtWidgets', name='QMessageBox'),
        Include(module='picard.plugin3.api', name='BaseAction'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'class MyAction(BaseAction):\n'
        )
        if i18n_support:
            text += '    TITLE = t_("action.title", "Plugin action")\n'
        else:
            text += '    TITLE = "Plugin action"\n'
        text += (
            '\n'
            '    def callback(self, objs):\n'
            '        self.api.logger.info(f"Action called with {len(objs)} objects")\n'
            '        for obj in objs:\n'
            '            self.api.logger.info(str(obj))\n'
            '\n'
            '        QMessageBox.information(\n'
            '            None,\n'
        )
        if i18n_support:
            text += (
                '            self.api.tr("action.dialog.title", "Plugin action"),\n'
                '            self.api.tr("action.dialog.text", "Action triggered"),\n'
            )
        else:
            text += (
                '            "Plugin action",\n'
                '            "Action triggered",\n'
            )
        text += '        )\n'
        return text


class CodeAlbumPostRemoval(CodeTemplate):
    registration_block = (
        '\n'
        '    # Album post-removal processor\n'
        '    api.register_album_post_removal_processor(album_post_removal_processor)\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='Album'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def album_post_removal_processor(api: PluginApi, album: Album):\n'
            '    api.logger.info(f"Album post removal processor: {album}")\n'
        )
        return text


class CodeFilePostLoad(CodeTemplate):
    registration_block = (
        '\n'
        '    # File post-load processor\n'
        '    api.register_file_post_load_processor(file_post_load_processor)\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='File'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def file_post_load_processor(api: PluginApi, file: File):\n'
            '    api.logger.info(f"File post load processor: {file}")\n'
        )
        return text


class CodeFilePostAddToTrack(CodeTemplate):
    registration_block = (
        '\n'
        '    # File post add to track processor\n'
        '    api.register_file_post_addition_to_track_processor(\n'
        '        file_post_addition_to_track_processor\n'
        '    )\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='File'),
        Include(module='picard.plugin3.api', name='Track'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def file_post_addition_to_track_processor(api: PluginApi, track: Track, file: File):\n'
            '    api.logger.info(f"File post addition to track processor: {track} <- {file}")\n'
        )
        return text


class CodeFilePostRemoveFromTrack(CodeTemplate):
    registration_block = (
        '\n'
        '    # File post remove from track processor\n'
        '    api.register_file_post_removal_from_track_processor(\n'
        '        file_post_removal_from_track_processor\n'
        '    )\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='File'),
        Include(module='picard.plugin3.api', name='Track'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def file_post_removal_from_track_processor(api: PluginApi, track: Track, file: File):\n'
            '    api.logger.info(f"File post removal from track processor: {track} -> {file}")\n'
        )
        return text


class CodeFilePreSave(CodeTemplate):
    registration_block = (
        '\n'
        '    # File pre-save processor\n'
        '    api.register_file_pre_save_processor(file_pre_save_processor)\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='File'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def file_pre_save_processor(api: PluginApi, file: File):\n'
            '    api.logger.info(f"File pre save processor: {file}")\n'
        )
        return text


class CodeFilePostSave(CodeTemplate):
    registration_block = (
        '\n'
        '    # File post-save processor\n'
        '    api.register_file_post_save_processor(file_post_save_processor)\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='File'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def file_post_save_processor(api: PluginApi, file: File):\n'
            '    api.logger.info(f"File post save processor: {file}")\n'
        )
        return text


class CodeScriptFunctions(CodeTemplate):
    registration_block = (
        '\n'
        '    # Scripting functions\n'
        '    api.register_script_function(func_playground_version, "playground_version")\n'
        '    api.register_script_function(func_playground_one_arg, "playground_one_arg")\n'
        '    api.register_script_function(func_playground_two_args, "playground_two_args")\n'
        '    api.register_script_function(func_playground_variadic, "playground_variadic")\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='ScriptParser'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'def func_playground_version(parser: ScriptParser) -> str:\n'
            '    api = PluginApi.get_api()\n'
            '    api.logger.info("Executed $playground_version()")\n'
            '    return f"{api.manifest.name()}: {api.manifest.version}"\n'
            '\n\n'
            'def func_playground_one_arg(parser: ScriptParser, arg1: str) -> str:\n'
            '    api = PluginApi.get_api()\n'
            '    api.logger.info(f"Executed $playground_test({arg1})")\n'
            '    return arg1.upper()\n'
            '\n\n'
            'def func_playground_two_args(parser: ScriptParser, arg1: str, arg2: str) -> str:\n'
            '    api = PluginApi.get_api()\n'
            '    api.logger.info(f"Executed $playground_test({arg1})")\n'
            '    return f"{arg1.upper()} & {arg2.lower()}"\n'
            '\n\n'
            'def func_playground_variadic(parser: ScriptParser, *args: str) -> str:\n'
            '    api = PluginApi.get_api()\n'
            '    api.logger.info(f"Executed $playground_test({\', \'.join(args)})")\n'
            '    return " & ".join(args)\n'
        )
        return text


class CodeScriptVariables(CodeTemplate):
    registration_block = (
        '\n'
        '    # Scripting variables\n'
        '    api.register_script_variable("playground", "Just a test tag / variable")\n'
        '    api.register_script_variable("_playground", "Just a test variable")\n'
    )
    includes = set()

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = ''
        return text


class CodeFileFormat(CodeTemplate):
    registration_block = (
        '\n'
        '    # File formats\n'
        '    api.register_format(MyFileFormat)\n'
    )
    includes = {
        Include(module='picard.plugin3.api', name='File'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            'class MyFileFormat(File):\n'
            '    EXTENSIONS = [".txt"]\n'
            '    NAME = "Text"\n'
            '\n'
            '    @classmethod\n'
            '    def supports_tag(cls, name: str) -> bool:\n'
            '        return False\n'
            '\n'
            '    def _load(self, filename: str) -> Metadata:\n'
            '        PluginApi.get_api().logger.info("Loading metadata from file %r", filename)\n'
            '        metadata = Metadata()\n'
            '        metadata["~format"] = self.NAME\n'
            '        return metadata\n'
            '\n'
            '    def _save(self, filename: str, metadata: Metadata) -> None:\n'
            '        PluginApi.get_api().logger.info("Saving metadata to file %r", filename)\n'
        )
        return text


class CodeOptionsPage(CodeTemplate):
    registration_block = (
        '\n'
        '    # Settings\n'
        '    api.plugin_config.register_option("run_image_processor", False)\n'
        '    api.plugin_config.register_option("my_choice", MyChoices.OPT2)\n'
        '\n'
        '    # Option page\n'
        '    api.register_options_page(MyOptionsPage)\n'
    )
    includes = {
        Include(module='enum', name='Enum'),
        Include(module='enum', name='auto'),
        Include(module='picard.plugin3.api', name='OptionsPage'),
        Include(module='.ui_options', name='Ui_PlaygroundOptionsPage'),
    }

    @classmethod
    def code_block(cls, i18n_support=False) -> str:
        text = (
            '\n\n'
            'class MyChoices(Enum):\n'
            '    OPT1 = auto()\n'
            '    OPT2 = auto()\n'
            '    OPT3 = auto()\n'
            '\n\n'
            'class MyOptionsPage(OptionsPage):\n'
            '    def __init__(self, parent=None):\n'
            '        super().__init__(parent)\n'
            '        self._ui = Ui_PlaygroundOptionsPage()\n'
            '        self._ui.setupUi(self)\n'
            '\n'
            '    def load(self):\n'
            '        self._ui.run_image_processor.setChecked(\n'
            '            bool(self.api.plugin_config["run_image_processor"])\n'
            '        )\n'
            '\n'
            '    def save(self):\n'
            '        self.api.plugin_config["run_image_processor"] = (\n'
            '            self._ui.run_image_processor.isChecked()\n'
            '        )\n'
        )
        return text


CODE_BLOCKS = OrderedDict(
    [
        ('metadata', {
            'name': t_("code_block.metadata", "Album/Track metadata processing"),
            'code_generator': CodeMetadata,
            'tooltip': t_(
                'ui.tooltip.code_template.metadata',
                'Code template for the MusicBrainz metadata post-processor hook, including both Album and Track processing examples.',
            ),
        }),

        ('action', {
            'name': t_("code_block.action", "Menu item"),
            'code_generator': CodeAction,
            'tooltip': t_(
                'ui.tooltip.code_template.action',
                (
                    'Code template for the hook used to add right-click context menu actions for albums, tracks and files in '
                    "'Unmatched Files', 'Clusters' and the 'ClusterList' (parent folder of Clusters). Actions can also "
                    'be added to the main Picard menu bar.'
                ),
            ),
        }),

        ('options', {
            'name': t_("code_block.options", "Options page and settings"),
            'code_generator': CodeOptionsPage,
            'tooltip': t_(
                'ui.tooltip.code_template.options',
                'Code template for adding plugin-specific user settings and an options page for managing the settings.',
            ),
        }),

        ('album_post_removal', {
            'name': t_("code_block.album_post_removal", "Album post-removal processing"),
            'code_generator': CodeAlbumPostRemoval,
            'tooltip': t_(
                'ui.tooltip.code_template.album_post_removal',
                'Code template for the hook called after an album has been removed from Picard.',
            ),
        }),

        ('file_post_load', {
            'name': t_("code_block.file_post_load", "File post-load processing"),
            'code_generator': CodeFilePostLoad,
            'tooltip': t_(
                'ui.tooltip.code_template.file_post_load',
                (
                    'Code template for the hook called after a file has been loaded into Picard. This could for example '
                    'be used to load additional data for a file.'
                ),
            ),
        }),

        ('file_post_add_track', {
            'name': t_("code_block.file_post_add_track", "File post add to track processing"),
            'code_generator': CodeFilePostAddToTrack,
            'tooltip': t_(
                'ui.tooltip.code_template.file_post_add_track',
                'Code template for the hook called after a file has been added to a track (on the right-hand pane of Picard).',
            ),
        }),

        ('file_post_remove_track', {
            'name': t_("code_block.file_post_remove_track", "File post remove from track processing"),
            'code_generator': CodeFilePostRemoveFromTrack,
            'tooltip': t_(
                'ui.tooltip.code_template.file_post_remove_track',
                'Code template for the hook called after a file has been removed from a track (on the right-hand pane of Picard).',
            ),
        }),

        ('file_pre_save', {
            'name': t_("code_block.file_pre_save", "File pre-save processing"),
            'code_generator': CodeFilePreSave,
            'tooltip': t_(
                'ui.tooltip.code_template.file_pre_save',
                (
                    'Code template for the hook called before a file has been saved. This can for example be '
                    'used to run additional pre-processing on the file.'
                ),
            ),
        }),

        ('file_post_save', {
            'name': t_("code_block.file_post_save", "File post-save processing"),
            'code_generator': CodeFilePostSave,
            'tooltip': t_(
                'ui.tooltip.code_template.file_post_save',
                (
                    'Code template for the hook called after a file has been saved. This can for example be used '
                    "to run additional post-processing on the file or write extra data. Note that the file's "
                    'metadata is already the newly saved metadata.'
                ),
            ),
        }),

        ('script_functions', {
            'name': t_("code_block.script_functions", "Scripting functions"),
            'code_generator': CodeScriptFunctions,
            'tooltip': t_(
                'ui.tooltip.code_template.script_functions',
                (
                    'Code template for adding new scripting functions to Picard, including examples with varying '
                    'numbers of arguments. This provides the descriptions used in the scripting auto-completion '
                    'and documentation.'
                ),
            ),
        }),

        ('script_variables', {
            'name': t_("code_block.script_variables", "Scripting variables"),
            'code_generator': CodeScriptVariables,
            'tooltip': t_(
                'ui.tooltip.code_template.script_variables',
                (
                    'Code template for adding new scripting variables to Picard, used to describe the variables in '
                    'the scripting auto-completion and documentation. This is often used in conjunction with '
                    'metadata processors that create new variables.'
                ),
            ),
        }),

        ('file_format', {
            'name': t_("code_block.format", "File format"),
            'code_generator': CodeFileFormat,
            'tooltip': t_(
                'ui.tooltip.code_template.file_format',
                (
                    'Code template to extend Picard with support for additional file formats. See the existing file '
                    'format implementations for details on how to implement the _load and _save methods.'
                ),
            ),
        }),
    ]
)


def generate_init(code_blocks: set[str], i18n_support: bool = False) -> str:
    """Generate the content for the __init__.py file.

    Args:
        code_blocks (set[str]): Code blocks to include.
        i18n_support (bool, optional): Whether to include translation support in the template. Defaults to False.

    Returns:
        str: Content for the __init__.py file.
    """
    includes = {'picard.plugin3.api': {'PluginApi'}}
    code_block = ""
    registration_block = (
        '\n\n'
        'def enable(api: PluginApi) -> None:\n'
        '    """Called when the plugin is enabled.\n'
        '\n'
        '    Use api to register plugin hooks and access essential Picard APIs.\n'
        '    """\n'
    )
    code_blocks_text = ""
    api = PluginApi.get_api()
    if i18n_support:
        includes['picard.plugin3.api'].add('t_')

    for block in sorted(code_blocks):
        if block not in CODE_BLOCKS:
            return f"Code block template '{block}' not found"

    for key in CODE_BLOCKS.keys():
        if key not in code_blocks:
            continue

        if not code_blocks_text:
            code_blocks_text = "# Includes example code blocks:\n"
        code_blocks_text += f"#    * {api.tr(CODE_BLOCKS[key]['name'])}\n"
        generator: CodeTemplate = CODE_BLOCKS[key]['code_generator']

        code_block += generator.code_block(i18n_support=i18n_support)
        registration_block += generator.registration_block
        for include in generator.includes:
            if include.module not in includes:
                includes[include.module] = set()
            includes[include.module].add(include.name)

    if not code_blocks_text:
        code_blocks_text = "# Base template only.  No specific code examples included.\n"
    else:
        code_blocks_text += (
            '#\n'
            "# Code examples provided by Philipp Wolfer\n"
            "# See https://git.sr.ht/~phw/picard-plugin-playground\n"
        )

    if not code_block:
        if i18n_support:
            code_block = (
                '\n'
                '# Module-level translatable strings (resolved at runtime via api.tr)\n'
                'GREETING = t_("message.greeting", "Hello from the plugin!")\n'
            )
            registration_block += (
                '\n'
                '    # Translate a string at runtime\n'
                '    greeting = api.tr(GREETING, "Hello from the plugin!")\n'
            )
        else:
            registration_block += (
                '\n'
                '    greeting = "Hello from the plugin!"\n'
            )
        registration_block += '    api.logger.info(greeting)\n'

    content = (
        '"""Picard 3 Plugin Framework"""\n\n'
        '# Automatically generated using "Create Local Plugin"\n\n'
    )
    content += code_blocks_text + '\n' + _make_includes_block(includes) + code_block + registration_block
    content += (
        '\n\n'
        'def disable() -> None:\n'
        '    """Called when the plugin is disabled."""\n'
        '    pass\n'
    )
    return content


def _make_includes_block(includes: dict[str, set[str]]) -> str:
    includes_block = ''
    old_module = ''
    for key in sorted(includes.keys()):
        if key:
            first_module = key.split('.')[0]
            if first_module != old_module:
                includes_block += '\n'
                old_module = first_module
            includes_block += f"from {key} "
        includes_block += "import "
        names = sorted(includes[key])
        if len(names) < 2:
            includes_block += f"{names[0]}\n"
        else:
            includes_block += "(\n"
            for name in names:
                includes_block += f"    {name},\n"
            includes_block += ")\n"
    return includes_block
