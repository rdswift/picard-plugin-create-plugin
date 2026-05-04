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


import os

from PyQt6 import QtWidgets

from picard.const.languages import UI_LANGUAGES
from picard.plugin3.api import (
    OptionsPage,
    PluginApi,
    t_,
)
from picard.plugin3.categories import (
    CATEGORIES_TITLES,
    category_title_i18n,
)

from .file_gitignore import write_gitignore
from .file_init import (
    CODE_TEMPLATES,
    write_init,
)
from .file_locale import write_locale
from .file_manifest import write_manifest
from .file_readme import write_readme
from .git_utils import initialize_git_repo
from .licenses import LICENSES
from .ui_plugin_dialog import Ui_CreatePluginOptionsPage
from .utils import is_directory_empty


USER_GUIDE_URL = 'https://picard-plugins-user-guides.readthedocs.io/en/latest/create_plugin/user_guide.html'

# Option settings
OPT_AUTHOR_NAME = 'author_name'
OPT_AUTHOR_EMAIL = 'author_email'
OPT_ROOT_DIRECTORY = 'root_directory'
OPT_LICENSE = 'license'
OPT_TRANSLATABLE = 'translatable'
OPT_BASE_LANGUAGE = 'base_language'
OPT_INITIAL_COMMIT = 'initial_commit'


class CreatePluginOptionsPage(OptionsPage):
    """Options page for the Create Local Plugin plugin.
    """

    TITLE = t_("ui.title", "Create Local Plugin")
    HELP_URL = USER_GUIDE_URL

    def __init__(self, parent=None):
        super(CreatePluginOptionsPage, self).__init__(parent)

        self.ui = Ui_CreatePluginOptionsPage()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface elements.
        """
        # Set open directory icon on folder browse button
        icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DirOpenIcon)
        self.ui.directory_browser.setIcon(icon)

        # Set up the categories section with checkboxes for each category
        row = 0
        col = 0
        for i, key in enumerate(CATEGORIES_TITLES.keys()):
            category = QtWidgets.QCheckBox()
            category.setText(category_title_i18n(key))
            category.setChecked(False)
            self.ui.categories_section_frame.layout().addWidget(category, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Set up the available base languages
        for language in UI_LANGUAGES:
            self.ui.base_language.addItem(language[2], language[0])

        # Set up the license options
        self.ui.plugin_license.addItem(self.api.tr('licenses.select', 'Select a license...'), '')
        for spdx_id, info in sorted(LICENSES.items(), key=lambda x: x[1]['name'].lower()):
            self.ui.plugin_license.addItem(self.api.tr(info['name']), spdx_id)

        # Set up the available plugin types
        for template_key, template_info in CODE_TEMPLATES.items():
            self.ui.plugin_type.addItem(self.api.tr(template_info['name']), template_key)

        self.ui.directory_browser.clicked.connect(self.select_plugin_directory)
        self.ui.button_create.clicked.connect(self.create_plugin)
        self.ui.button_clear.clicked.connect(self.load)

    def load(self):
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
        base_locale = self.api.plugin_config[OPT_BASE_LANGUAGE]
        if not base_locale:
            base_locale = self.api.get_locale()
        base_locale_index = self.ui.base_language.findData(base_locale)
        if base_locale_index == -1:
            base_locale_index = self.ui.base_language.findData('en')
        self.ui.base_language.setCurrentIndex(max(base_locale_index, 0))
        self.ui.plugin_title.clear()
        self.ui.plugin_description.clear()
        for i in range(self.ui.categories_section_frame.layout().count()):
            widget = self.ui.categories_section_frame.layout().itemAt(i).widget()
            widget.setChecked(False)
        self.ui.plugin_type.setCurrentIndex(0)

    def save(self):
        """Save the option settings.
        """
        self.api.plugin_config[OPT_AUTHOR_NAME] = self.ui.plugin_author_name.text().strip()
        self.api.plugin_config[OPT_AUTHOR_EMAIL] = self.ui.plugin_author_email.text().strip()
        self.api.plugin_config[OPT_ROOT_DIRECTORY] = self.base_directory
        self.api.plugin_config[OPT_LICENSE] = self.ui.plugin_license.currentData()
        self.api.plugin_config[OPT_TRANSLATABLE] = self.ui.tx_enabled.isChecked()
        self.api.plugin_config[OPT_BASE_LANGUAGE] = self.ui.base_language.currentData()
        self.api.plugin_config[OPT_INITIAL_COMMIT] = self.ui.enter_initial_commit.isChecked()

    def confirm_creation(self) -> bool:
        """Show a confirmation dialog before creating the plugin.

        Returns:
            bool: True if the user confirms, False otherwise.
        """
        categories = self.get_categories_list()

        return QtWidgets.QMessageBox.question(
            self,
            self.api.tr('ui.confirm_creation', 'Confirm Plugin Creation'),
            self.api.tr(
                'ui.confirm_creation_message',
                (
                    "Please confirm that the target directory is correct before proceeding.\n\n"
                    "Directory: {directory}\n\n"
                    "Are you sure you want to create the plugin with the provided settings?\n\n"
                    "Title: {title}\n"
                    "Template: {template}\n"
                    "Categories: {categories}\n"
                    "License: {license}"
                )
            ).format(
                directory=self.ui.plugin_directory.text().strip(),
                title=self.ui.plugin_title.text().strip(),
                template=self.ui.plugin_type.currentText(),
                categories=', '.join(category_title_i18n(cat) for cat in categories) if categories else self.api.tr('ui.categories_none', 'None'),
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
        for i in range(self.ui.categories_section_frame.layout().count()):
            widget = self.ui.categories_section_frame.layout().itemAt(i).widget()
            if isinstance(widget, QtWidgets.QCheckBox) and widget.isChecked():
                category_text = widget.text()
                for key, title in CATEGORIES_TITLES.items():
                    if category_text == category_title_i18n(key):
                        categories.append(key)
                        break

        return categories

    def create_plugin(self):
        """Create the plugin based on the provided settings.
        """
        self.err_message = ""
        if not self.validate_settings():
            return

        if not self.confirm_creation():
            return

        plugin_name = self.ui.plugin_title.text().strip()
        plugin_directory = self.ui.plugin_directory.text().strip().rstrip('/\\')
        author_name = self.ui.plugin_author_name.text().strip()
        author_email = self.ui.plugin_author_email.text().strip()
        initial_commit = self.ui.enter_initial_commit.isChecked()

        self.api.logger.debug(f'Creating plugin "{plugin_name}" at directory: {plugin_directory}')
        if not self.write_plugin_files():
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

        self.base_directory = os.path.normpath(os.path.dirname(plugin_directory))

        self.save()
        self.load()

        self.api.logger.info(f"Plugin \"{plugin_name}\" created successfully at: {plugin_directory}")

        self.err_message = initialize_git_repo(
            plugin_dir=plugin_directory,
            name=author_name,
            email=author_email,
            initial_commit=initial_commit,
        )
        if self.err_message:
            self.api.logger.error(self.err_message)
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.git_initialization_failed', 'Git Initialization Failed'),
                self.api.tr(
                    'ui.error.git_initialization_failed_message',
                    "The plugin was created and the git repository initialized, but there was an error initializing the git repository.",
                ) + f"\n\nError details: {self.err_message}",
            )
            return

        self.api.logger.info(f"Plugin \"{plugin_name}\" git repository created successfully at: {plugin_directory}")

        QtWidgets.QMessageBox.information(
            self,
            self.api.tr('ui.success.creation_complete', 'Plugin Creation Complete'),
            self.api.tr('ui.success.creation_complete_message', 'The plugin has been created successfully.'),
        )

    def validate_settings(self) -> bool:
        """Validate the provided settings before creating the plugin.
        """
        outdir = self.ui.plugin_directory.text().strip()
        if not outdir:
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.missing_directory', 'Missing Directory'),
                self.api.tr('ui.error.missing_directory_message', 'No output directory specified. Please select a target directory for the plugin.'),
            )
            return False

        outdir = os.path.normpath(outdir)
        try:
            os.makedirs(outdir, exist_ok=True)

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.invalid_directory', 'Invalid Directory'),
                self.api.tr('ui.error.create_directory_message', 'Unable to create the target directory.') + f"\n\nError details: {e}",
            )
            return False

        if not os.path.isdir(outdir):
            QtWidgets.QMessageBox.warning(
                self,
                self.api.tr('ui.error.invalid_directory', 'Invalid Directory'),
                self.api.tr('ui.error.missing_directory_message', 'The target directory does not exist.'),
            )
            return False

        if not is_directory_empty(outdir):
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

    def write_plugin_files(self) -> bool:
        """Write the plugin files to the target directory.
        """
        author = self.ui.plugin_author_name.text().strip()
        email = self.ui.plugin_author_email.text().strip()
        name = self.ui.plugin_title.text().strip()
        description = self.ui.plugin_description.toPlainText().strip()
        license = self.ui.plugin_license.currentData()
        license_info = LICENSES.get(license, {})
        license_url = license_info.get('url', None)
        outdir = os.path.normpath(self.ui.plugin_directory.text().strip())
        base_locale = self.ui.base_language.currentData() or 'en'
        categories = self.get_categories_list()
        plugin_type = self.ui.plugin_type.currentData()
        i18n_support = self.ui.tx_enabled.isChecked()

        # Write .gitignore file
        self.api.logger.debug(f"Writing {os.path.join(outdir, '.gitignore')}")
        self.err_message = write_gitignore(outdir)
        if self.err_message:
            return False

        # Write README.md file
        self.api.logger.debug(f"Writing {os.path.join(outdir, 'README.md')}")
        self.err_message = write_readme(outdir, name, description)
        if self.err_message:
            return False

        # Write MANIFEST.toml file
        self.api.logger.debug(f"Writing {os.path.join(outdir, 'MANIFEST.toml')}")
        self.err_message = write_manifest(
            plugin_dir=outdir,
            name=name,
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
        self.api.logger.debug(f"Writing {os.path.join(outdir, '__init__.py')}")
        self.err_message = write_init(outdir, plugin_type, i18n_support)
        if self.err_message:
            return False

        # Write locale *.toml files
        if i18n_support:
            self.api.logger.debug(f"Writing locale files to {os.path.join(outdir, 'locale')}")
            self.err_message = write_locale(outdir, name, description, base_locale, plugin_type)
            if self.err_message:
                return False

        return True

    def select_plugin_directory(self):
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


def enable(api: PluginApi):
    """Called when plugin is enabled."""
    # Initialize settings
    api.plugin_config.register_option(OPT_AUTHOR_NAME, '')
    api.plugin_config.register_option(OPT_AUTHOR_EMAIL, '')
    api.plugin_config.register_option(OPT_ROOT_DIRECTORY, '')
    api.plugin_config.register_option(OPT_LICENSE, '')
    api.plugin_config.register_option(OPT_TRANSLATABLE, False)
    api.plugin_config.register_option(OPT_INITIAL_COMMIT, True)
    api.plugin_config.register_option(OPT_BASE_LANGUAGE, '')

    api.register_options_page(CreatePluginOptionsPage)
