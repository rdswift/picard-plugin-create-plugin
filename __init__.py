# -*- coding: utf-8 -*-
"""Create Local Plugin
"""
# Copyright (C) 2026 Bob Swift (rdswift)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

# Code examples for the generated __init__.py file are based on the
# playgound / testing plugin by Philipp Wolfer.
# See https://git.sr.ht/~phw/picard-plugin-playground

import os

from PyQt6 import QtWidgets

from picard.const.languages import UI_LANGUAGES
from picard.git.factory import git_backend
from picard.plugin3.api import (
    OptionsPage,
    PluginApi,
    t_,
)
from picard.plugin3.categories import (
    CATEGORIES_TITLES,
    category_title_i18n,
)
from picard.util import open_local_path

from .file_gitignore import write_gitignore
from .file_init import (
    CODE_BLOCKS,
    write_init,
)
from .file_locale import write_locale
from .file_manifest import write_manifest
from .file_readme import write_readme
from .file_ui import write_ui
from .licenses import LICENSES
from .ui_plugin_dialog import Ui_CreatePluginOptionsPage
from .ui_utils import (
    CATEGORY_TOOLTIPS,
    NO_DESCRIPTION,
)
from .utils import (
    is_directory_empty,
    slugify,
)


USER_GUIDE_URL = 'https://picard-plugins-user-guides.readthedocs.io/en/latest/create_plugin/user_guide.html'

# Option settings
OPT_AUTHOR_NAME = 'author_name'
OPT_AUTHOR_EMAIL = 'author_email'
OPT_ROOT_DIRECTORY = 'root_directory'
OPT_LICENSE = 'license'
OPT_TRANSLATABLE = 'translatable'
OPT_BASE_LANGUAGE = 'base_language'
OPT_INITIAL_COMMIT = 'initial_commit'
OPT_OPEN_DIRECTORY = 'open_dir_on_create'
OPT_CATEGORIES = 'categories'
OPT_TEMPLATES = 'templates'


class CreatePluginOptionsPage(OptionsPage):
    """Options page for the Create Local Plugin plugin.
    """

    TITLE = t_("ui.title", "Create Local Plugin")
    HELP_URL = USER_GUIDE_URL

    def __init__(self, parent=None) -> None:
        super(CreatePluginOptionsPage, self).__init__(parent)
        self.ui = Ui_CreatePluginOptionsPage()
        self.ui.setupUi(self)

        self.selected_templates = []
        self.categories_map = {}
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface elements.
        """
        # Set open directory icon on folder browse button
        icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DirOpenIcon)
        self.ui.directory_browser.setIcon(icon)

        # Set up the categories section with checkboxes for each category
        row = 0
        col = 0
        for key in CATEGORIES_TITLES.keys():
            category = QtWidgets.QCheckBox()
            category.setText(category_title_i18n(key))
            category.setChecked(False)
            tooltip = self.api.tr(CATEGORY_TOOLTIPS[key]) if key in CATEGORY_TOOLTIPS else self.api.tr(NO_DESCRIPTION)
            category.setToolTip(tooltip)
            self.categories_map[key] = category
            self.ui.categories_section_frame.layout().addWidget(category, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Set up the available base languages
        for language in UI_LANGUAGES:
            self.ui.base_language.addItem(language[2], language[0])

        # Set up the license options
        self.ui.plugin_license.addItem(self.api.tr('licenses.select', 'Select a license…'), '')
        for spdx_id, info in sorted(LICENSES.items(), key=lambda x: x[1]['name'].lower()):
            self.ui.plugin_license.addItem(self.api.tr(info['name']), spdx_id)

        # Set up the button connections
        self.ui.directory_browser.clicked.connect(self.select_plugin_directory)
        self.ui.button_create.clicked.connect(self.create_plugin)
        self.ui.button_clear.clicked.connect(self.load)
        self.ui.button_select_plugin_types.clicked.connect(self.open_code_selector_dialog)

    def load(self) -> None:
        """Load the option settings.
        """
        self.ui.plugin_author_name.setText(self.api.plugin_config[OPT_AUTHOR_NAME])
        self.ui.plugin_author_email.setText(self.api.plugin_config[OPT_AUTHOR_EMAIL])
        self.base_directory = self.api.plugin_config[OPT_ROOT_DIRECTORY]
        self.ui.plugin_directory.setText(self.base_directory)
        license_index = self.ui.plugin_license.findData(self.api.plugin_config[OPT_LICENSE])
        self.ui.plugin_license.setCurrentIndex(max(license_index, 0))
        self.ui.tx_enabled.setChecked(self.api.plugin_config[OPT_TRANSLATABLE])
        self.ui.enter_initial_commit.setChecked(self.api.plugin_config[OPT_INITIAL_COMMIT])
        self.ui.open_plugin_directory.setChecked(self.api.plugin_config[OPT_OPEN_DIRECTORY])
        base_locale = self.api.plugin_config[OPT_BASE_LANGUAGE]
        if not base_locale:
            base_locale = self.api.get_locale()
        base_locale_index = self.ui.base_language.findData(base_locale)
        if base_locale_index == -1:
            base_locale_index = self.ui.base_language.findData('en')
        self.ui.base_language.setCurrentIndex(max(base_locale_index, 0))
        self.ui.plugin_title.clear()
        self.ui.plugin_description.clear()
        for key, category in self.categories_map.items():
            category.setChecked(key in self.api.plugin_config[OPT_CATEGORIES])
        self.selected_templates = self.api.plugin_config[OPT_TEMPLATES]
        self._update_template_count()

    def save(self) -> None:
        """Save the option settings.
        """
        self.api.plugin_config[OPT_AUTHOR_NAME] = self.ui.plugin_author_name.text().strip()
        self.api.plugin_config[OPT_AUTHOR_EMAIL] = self.ui.plugin_author_email.text().strip()
        self.api.plugin_config[OPT_ROOT_DIRECTORY] = self.base_directory
        self.api.plugin_config[OPT_LICENSE] = self.ui.plugin_license.currentData()
        self.api.plugin_config[OPT_TRANSLATABLE] = self.ui.tx_enabled.isChecked()
        self.api.plugin_config[OPT_BASE_LANGUAGE] = self.ui.base_language.currentData()
        self.api.plugin_config[OPT_INITIAL_COMMIT] = self.ui.enter_initial_commit.isChecked()
        self.api.plugin_config[OPT_OPEN_DIRECTORY] = self.ui.open_plugin_directory.isChecked()
        self.api.plugin_config[OPT_CATEGORIES] = self.get_categories_list()
        self.api.plugin_config[OPT_TEMPLATES] = self.selected_templates

    def confirm_creation(self, plugin_name: str, plugin_dir: str) -> bool:
        """Show a confirmation dialog before creating the plugin.

        Args:
            plugin_name (str): Name of the plugin.
            plugin_dir (str): Directory to use for the plugin.

        Returns:
            bool: True if the user confirms, False otherwise.
        """
        categories = self.get_categories_list()
        templates = self.selected_templates
        none_text = self.api.tr('ui.categories_none', 'None')

        return QtWidgets.QMessageBox.question(
            self,
            self.api.tr('ui.confirm_creation', 'Confirm Plugin Creation'),
            self.api.tr(
                'ui.confirm_creation_message',
                (
                    "Are you sure you want to create the plugin with the provided settings?\n\n"
                    "Title: {title}\n\n"
                    "Directory: {directory}\n\n"
                    "Categories: {categories}\n\n"
                    "Templates: {templates}\n\n"
                    "License: {license}"
                ),
                title=plugin_name,
                directory=plugin_dir,
                categories='; '.join(category_title_i18n(cat) for cat in categories) if categories else none_text,
                templates='; '.join(self.api.tr(CODE_BLOCKS[cat]['name']) for cat in sorted(templates)) if templates else none_text,
                license=self.ui.plugin_license.currentText(),
            ),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        ) == QtWidgets.QMessageBox.StandardButton.Yes

    def get_categories_list(self) -> list[str]:
        """Get the list of selected categories.

        Returns:
            list[str]: List of selected category keys.
        """
        categories = []
        for key, category in self.categories_map.items():
            if category.isChecked():
                categories.append(key)

        return categories

    def create_plugin(self) -> None:
        """Create the plugin based on the provided settings.
        """
        plugin_name = self.ui.plugin_title.text().strip()
        plugin_name_slug = slugify(plugin_name) or 'unknown'
        plugin_directory = os.path.join(self.ui.plugin_directory.text().strip().rstrip('/\\'), f"picard-plugin-{plugin_name_slug}")

        self.err_message = ""
        if not self.validate_settings(plugin_directory):
            return

        if not self.confirm_creation(plugin_name, plugin_directory):
            return

        author_name = self.ui.plugin_author_name.text().strip()
        author_email = self.ui.plugin_author_email.text().strip()
        initial_commit = self.ui.enter_initial_commit.isChecked()

        self.api.logger.debug(f'Creating plugin "{plugin_name}" at directory: {plugin_directory}')
        if not self.write_plugin_files(plugin_name, plugin_directory):
            if self.err_message:
                self.api.logger.error(self.err_message)
                self.err_message = "\n\n" + self.err_message
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.creation_failed', 'Plugin Creation Failed'),
                self.api.tr(
                    'ui.error.creation_failed_message',
                    "An error occurred while creating the plugin. Please check the target directory and try again."
                ) + (self.err_message or ""),
            )
            return

        self.save()     # Save the current settings to use for future plugins

        self.api.logger.info(f'Plugin "{plugin_name}" created successfully at: {plugin_directory}')

        self.err_message = self.initialize_git_repo(
            plugin_dir=plugin_directory,
            name=author_name,
            email=author_email,
            initial_commit=initial_commit,
        )

        if self.err_message:
            self.api.logger.error(f"Error initializing git repository: {self.err_message}")
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.git_initialization_failed', 'Git Initialization Failed'),
                self.api.tr(
                    'ui.error.git_initialization_failed_message',
                    (
                        "The plugin was created but there was an error initializing the "
                        "git repository.\n\nError details: {err_message}"
                    ),
                    err_message=self.err_message,
                ),
            )
            self.open_created_plugin_dir(plugin_directory)
            return

        self.api.logger.info(f'Plugin "{plugin_name}" git repository created successfully at: {plugin_directory}')

        QtWidgets.QMessageBox.information(
            self,
            self.api.tr('ui.success.creation_complete', 'Plugin Creation Complete'),
            self.api.tr('ui.success.creation_complete_message', 'The plugin has been created successfully.'),
        )

        self.open_created_plugin_dir(plugin_directory)

    def open_created_plugin_dir(self, plugin_dir: str) -> None:
        """Opens the newly created plugin directory in the user's file browser.

        Args:
            plugin_dir (str): Directory to open.
        """
        if self.ui.open_plugin_directory.isChecked():
            open_local_path(plugin_dir)

    def validate_settings(self, plugin_dir: str) -> bool:
        """Validate the provided settings before creating the plugin.

        Args:
            plugin_dir (str): Directory to validate.

        Returns (bool): True on success, otherwise False.
        """
        if not self.ui.plugin_directory.text().strip():
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.missing_directory', 'Missing Directory'),
                self.api.tr(
                    'ui.error.missing_root_directory_message',
                    'No output root directory specified. Please select a target parent directory for the plugin directory creation.'
                ),
            )
            return False

        try:
            os.makedirs(plugin_dir, exist_ok=True)

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.invalid_directory', 'Invalid Directory'),
                self.api.tr(
                    'ui.error.create_directory_message',
                    'Unable to create the target directory.\n\nError details: {error}',
                    error=e
                ),
            )
            return False

        if not os.path.isdir(plugin_dir):
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.invalid_directory', 'Invalid Directory'),
                self.api.tr('ui.error.missing_directory_message', 'The target directory for the plugin does not exist.'),
            )
            return False

        if not is_directory_empty(plugin_dir):
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.invalid_directory', 'Invalid Directory'),
                self.api.tr('ui.error.directory_not_empty_message', 'The target directory is not empty.'),
            )
            return False

        if not self.ui.plugin_title.text().strip():
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.missing_title', 'Missing Plugin Title'),
                self.api.tr('ui.error.missing_title_message', 'Please enter a title for the plugin.'),
            )
            return False

        if not self.ui.plugin_author_name.text().strip():
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.missing_author_name', 'Missing Author Name'),
                self.api.tr('ui.error.missing_author_name_message', "Please enter the author's name."),
            )
            return False

        if not self.ui.plugin_author_email.text().strip():
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.missing_author_email', 'Missing Author Email'),
                self.api.tr('ui.error.missing_author_email_message', "Please enter the author's email address."),
            )
            return False

        if not self.ui.plugin_description.toPlainText().strip():
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.missing_description', 'Missing Plugin Description'),
                self.api.tr('ui.error.missing_description_message', 'Please enter a description for the plugin.'),
            )
            return False

        return True

    def write_plugin_files(self, plugin_name: str, plugin_dir: str) -> bool:
        """Write the plugin files to the target directory.

        Args:
            plugin_name (str): Name of the plugin.
            plugin_dir (str): Directory to use for the plugin.

        Returns (bool): True on success, otherwise False.
        """
        author = self.ui.plugin_author_name.text().strip()
        email = self.ui.plugin_author_email.text().strip()
        description = self.ui.plugin_description.toPlainText().strip()
        license = self.ui.plugin_license.currentData()
        license_info = LICENSES.get(license, {})
        license_url = license_info.get('url', None)
        base_locale = self.ui.base_language.currentData() or 'en'
        categories = self.get_categories_list()
        i18n_support = self.ui.tx_enabled.isChecked() or 'options' in self.selected_templates

        # Write .gitignore file
        self.api.logger.debug(f"Writing {os.path.join(plugin_dir, '.gitignore')}")
        self.err_message = write_gitignore(plugin_dir)
        if self.err_message:
            return False

        # Write README.md file
        self.api.logger.debug(f"Writing {os.path.join(plugin_dir, 'README.md')}")
        self.err_message = write_readme(plugin_dir, plugin_name, description)
        if self.err_message:
            return False

        # Write MANIFEST.toml file
        self.api.logger.debug(f"Writing {os.path.join(plugin_dir, 'MANIFEST.toml')}")
        self.err_message = write_manifest(
            plugin_dir=plugin_dir,
            name=plugin_name,
            description=description,
            author=author,
            email=email,
            license=license,
            license_url=license_url,
            categories=categories,
            base_locale=base_locale if i18n_support else None,
        )
        if self.err_message:
            return False

        # Write __init__.py file
        self.api.logger.debug(f"Writing {os.path.join(plugin_dir, '__init__.py')}")
        self.err_message = write_init(plugin_dir, self.selected_templates, i18n_support)
        if self.err_message:
            return False

        # Write UI files
        if 'options' in self.selected_templates:
            self.api.logger.debug(f"Writing UI files to {plugin_dir}")
            self.err_message = write_ui(plugin_dir)
            if self.err_message:
                return False

        # Write locale *.toml files
        if i18n_support:
            self.api.logger.debug(f"Writing locale files to {os.path.join(plugin_dir, 'locale')}")
            self.err_message = write_locale(plugin_dir, plugin_name, description, base_locale, self.selected_templates)
            if self.err_message:
                return False

        return True

    def initialize_git_repo(self, plugin_dir: str, name: str, email: str, initial_commit: bool) -> str | None:
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
            return str(e)

        return None

    def select_plugin_directory(self) -> None:
        """Open a directory selection dialog to choose the plugin root directory.
        """
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            self.api.tr('ui.select_directory', 'Select Plugin Root Directory'),
            self.ui.plugin_directory.text().strip() or os.path.expanduser('~'),
            QtWidgets.QFileDialog.Option.ShowDirsOnly,
        )
        if directory:
            self.ui.plugin_directory.setText(os.path.normpath(directory))

    def _update_template_count(self) -> None:
        """Update the count of the selected code templates.
        """
        self.ui.label_plugin_type_count.setText(
            self.api.trn('template_count', "{n} template selected", "{n} templates selected", n=len(self.selected_templates))
        )

    def open_code_selector_dialog(self) -> None:
        """Open the dialog to allow selection of code templates to include in the generated plugin.
        """
        dialog = CodeTemplateSelectionDialog(self.selected_templates, self.api, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.selected_templates = dialog.get_selected_templates()
            self._update_template_count()


class CodeTemplateSelectionDialog(QtWidgets.QDialog):
    """Dialog for selecting code templates to include in the plugin.
    """
    def __init__(self, templates: set[str], api: PluginApi, parent=None) -> None:
        """_summary_

        Args:
            templates (set[str]): Currently selected code templates
            api (PluginApi): Current plugin api
            parent (optional): Parent widget. Defaults to None.
        """
        super().__init__(parent=parent)
        self.templates: set = templates
        self.api: PluginApi = api
        self.options_map = {}
        self.setup_dialog()

    def setup_dialog(self) -> None:
        self.setWindowTitle(self.api.tr('selector_dialog.title', 'Selected Templates'))

        message = QtWidgets.QLabel(self.api.tr('selector_dialog.message', 'Select the desired code templates to include:'))

        selection_items_frame = QtWidgets.QFrame()
        selection_items_frame.setFrameStyle(QtWidgets.QFrame.Shape.Box | QtWidgets.QFrame.Shadow.Plain)
        selection_items_frame.setLineWidth(1)
        self.selection_items = QtWidgets.QVBoxLayout()
        for key, value in CODE_BLOCKS.items():
            checkbox = QtWidgets.QCheckBox(self.api.tr(value['name']))
            checkbox.setChecked(key in self.templates)
            checkbox.setToolTip(self.api.tr(value['tooltip']))
            self.options_map[key] = checkbox
            self.selection_items.addWidget(checkbox)
        selection_items_frame.setLayout(self.selection_items)

        self.bbox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        self.bbox.accepted.connect(self.accept)
        self.bbox.rejected.connect(self.reject)

        dialog_layout = QtWidgets.QVBoxLayout()
        dialog_layout.addWidget(message)
        dialog_layout.addWidget(selection_items_frame)
        dialog_layout.addWidget(self.bbox)

        self.setLayout(dialog_layout)

    def get_selected_templates(self) -> list[str]:
        selected_templates = []
        for key, value in self.options_map.items():
            if value.isChecked():
                selected_templates.append(key)
        return selected_templates


def enable(api: PluginApi) -> None:
    """Called when plugin is enabled."""
    # Initialize settings
    api.plugin_config.register_option(OPT_AUTHOR_NAME, '')
    api.plugin_config.register_option(OPT_AUTHOR_EMAIL, '')
    api.plugin_config.register_option(OPT_ROOT_DIRECTORY, '')
    api.plugin_config.register_option(OPT_LICENSE, '')
    api.plugin_config.register_option(OPT_TRANSLATABLE, False)
    api.plugin_config.register_option(OPT_INITIAL_COMMIT, True)
    api.plugin_config.register_option(OPT_BASE_LANGUAGE, '')
    api.plugin_config.register_option(OPT_OPEN_DIRECTORY, False)
    api.plugin_config.register_option(OPT_CATEGORIES, [])
    api.plugin_config.register_option(OPT_TEMPLATES, [])

    api.register_options_page(CreatePluginOptionsPage)
