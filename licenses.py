"""SPDX License List (Partial)
"""

from picard.plugin3.api import t_

LICENSES = {
    'Apache-2.0': {
        'name': t_('licenses.Apache-2.0', 'Apache License 2.0'),
        'url': 'https://www.apache.org/licenses/LICENSE-2.0',
    },
    'BSD-2-Clause': {
        'name': t_('licenses.BSD-2-Clause', 'BSD 2-Clause "Simplified" License'),
        'url': 'https://opensource.org/license/BSD-2-Clause',
    },
    'BSD-3-Clause': {
        'name': t_('licenses.BSD-3-Clause', 'BSD 3-Clause "New" or "Revised" License'),
        'url': 'https://opensource.org/license/BSD-3-Clause',
    },
    'GPL-2.0-or-later': {
        'name': t_('licenses.GPL-2.0-or-later', 'GNU General Public License v2.0 or later'),
        'url': 'https://www.gnu.org/licenses/old-licenses/gpl-2.0.html',
    },
    'GPL-3.0-or-later': {
        'name': t_('licenses.GPL-3.0-or-later', 'GNU General Public License v3.0 or later'),
        'url': 'https://www.gnu.org/licenses/gpl-3.0.html',
    },
    'MIT': {
        'name': t_('licenses.MIT', 'MIT License'),
        'url': 'https://opensource.org/license/MIT',
    },
    'other': {
        'name': t_('licenses.other', 'Proprietary or Other (enter manually in MANIFEST)'),
        'url': None,
    },
}
