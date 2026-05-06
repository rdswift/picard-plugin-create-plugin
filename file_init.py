"""Plugin __init__.py file generation
"""
# Code examples for the __init__.py file are based on the playgound / testing plugin by Philipp Wolfer.
# See https://git.sr.ht/~phw/picard-plugin-playground

from collections import (
    OrderedDict,
    namedtuple,
)
import os

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
        Include(module='PyQt6', name='QtCore'),
        Include(module='PyQt6', name='QtGui'),
        Include(module='PyQt6', name='QtWidgets'),
        Include(module='picard.plugin3.api', name='OptionsPage'),
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
            'class Ui_PlaygroundOptionsPage(object):\n'
            '    def setupUi(self, PlaygroundOptionsPage):\n'
            '        PlaygroundOptionsPage.setObjectName("PlaygroundOptionsPage")\n'
            '        PlaygroundOptionsPage.resize(602, 555)\n'
            '        self.vboxlayout = QtWidgets.QVBoxLayout(PlaygroundOptionsPage)\n'
            '        self.vboxlayout.setContentsMargins(9, 9, 9, 9)\n'
            '        self.vboxlayout.setSpacing(6)\n'
            '        self.vboxlayout.setObjectName("vboxlayout")\n'
            '        self.groupBox = QtWidgets.QGroupBox(parent=PlaygroundOptionsPage)\n'
            '        self.groupBox.setObjectName("groupBox")\n'
            '        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.groupBox)\n'
            '        self.vboxlayout1.setContentsMargins(9, 9, 9, 9)\n'
            '        self.vboxlayout1.setSpacing(2)\n'
            '        self.vboxlayout1.setObjectName("vboxlayout1")\n'
            '        self.xqaf_compression_disabled_note = QtWidgets.QFrame(parent=self.groupBox)\n'
            '        self.xqaf_compression_disabled_note.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)\n'
            '        self.xqaf_compression_disabled_note.setObjectName("xqaf_compression_disabled_note")\n'
            '        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.xqaf_compression_disabled_note)\n'
            '        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)\n'
            '        self.verticalLayout_3.setSpacing(0)\n'
            '        self.verticalLayout_3.setObjectName("verticalLayout_3")\n'
            '        self.frame_2 = QtWidgets.QFrame(parent=self.xqaf_compression_disabled_note)\n'
            '        self.frame_2.setStyleSheet("QFrame { background-color: #ffc107; color: black }\\nQCheckBox { color: black }")\n'
            '        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)\n'
            '        self.frame_2.setObjectName("frame_2")\n'
            '        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)\n'
            '        self.verticalLayout_2.setObjectName("verticalLayout_2")\n'
            '        self.label = QtWidgets.QLabel(parent=self.frame_2)\n'
            '        self.label.setWordWrap(True)\n'
            '        self.label.setObjectName("label")\n'
            '        self.verticalLayout_2.addWidget(self.label)\n'
            '        self.verticalLayout_3.addWidget(self.frame_2)\n'
            '        spacerItem = QtWidgets.QSpacerItem(1, 6, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)\n'
            '        self.verticalLayout_3.addItem(spacerItem)\n'
            '        self.vboxlayout1.addWidget(self.xqaf_compression_disabled_note)\n'
            '        self.run_image_processor = QtWidgets.QCheckBox(parent=self.groupBox)\n'
            '        self.run_image_processor.setObjectName("run_image_processor")\n'
            '        self.vboxlayout1.addWidget(self.run_image_processor)\n'
            '        self.vboxlayout.addWidget(self.groupBox)\n'
            '        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)\n'
            '        self.vboxlayout.addItem(spacerItem1)\n'
            '\n'
            '        self.groupBox.setTitle("API Playground options")\n'
            '        self.label.setText("This is not a real plugin. It only exists to try the implementation of as much of Picard\'s plugin API as possible.")\n'
            '        self.run_image_processor.setText("Run image processor. This applies a sepia effect on all loaded cover images.")\n'
            '\n'
            '        QtCore.QMetaObject.connectSlotsByName(PlaygroundOptionsPage)\n'
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
        }),

        ('action', {
            'name': t_("code_block.action", "Menu item"),
            'code_generator': CodeAction,
        }),

        ('options', {
            'name': t_("code_block.options", "Options page and settings"),
            'code_generator': CodeOptionsPage,
        }),

        ('album_post_removal', {
            'name': t_("code_block.album_post_removal", "Album post-removal processing"),
            'code_generator': CodeAlbumPostRemoval,
        }),

        ('file_post_load', {
            'name': t_("code_block.file_post_load", "File post-load processing"),
            'code_generator': CodeFilePostLoad,
        }),

        ('file_post_add_track', {
            'name': t_("code_block.file_post_add_track", "File post add to track processing"),
            'code_generator': CodeFilePostAddToTrack,
        }),

        ('file_post_remove_track', {
            'name': t_("code_block.file_post_remove_track", "File post remove from track processing"),
            'code_generator': CodeFilePostRemoveFromTrack,
        }),

        ('file_pre_save', {
            'name': t_("code_block.file_pre_save", "File pre-save processing"),
            'code_generator': CodeFilePreSave,
        }),

        ('file_post_save', {
            'name': t_("code_block.file_post_save", "File post-save processing"),
            'code_generator': CodeFilePostSave,
        }),

        ('script_functions', {
            'name': t_("code_block.script_functions", "Scripting functions"),
            'code_generator': CodeScriptFunctions,
        }),

        ('script_variables', {
            'name': t_("code_block.script_variables", "Scripting variables"),
            'code_generator': CodeScriptVariables,
        }),

        ('file_format', {
            'name': t_("code_block.format", "File format"),
            'code_generator': CodeFileFormat,
        }),
    ]
)


def write_init(plugin_dir: str, code_blocks: set, i18n_support: bool = False) -> str | None:
    """Write the __init__.py file.

    Args:
        plugin_dir (str): Plugin directory
        templates (set): Code blocks to include
        i18n_support (bool): Whether to include translation support in the template

    Returns:
        str | None: Error message or None if successful
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
    try:
        with open(os.path.join(plugin_dir, '__init__.py'), 'w', encoding='utf8') as f:
            f.write(content)
    except OSError as e:
        return f"Error writing '__init__.py': {e}"

    return None


def _make_includes_block(includes: dict[str, set]) -> str:
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
