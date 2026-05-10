"""Picard pluigin categries
"""

from picard.plugin3.api import t_


NO_DESCRIPTION = t_('ui.text.no_description', 'No description available.')

CATEGORY_TOOLTIPS = {
    'coverart': t_(
        'ui.tooltip.categories.coverart',
        (
            'The plugin provides cover art related processing, such as adding a new cover art '
            'source.'
        ),
    ),
    'formats': t_(
        'ui.tooltip.categories.formats',
        (
            'The plugin provides additional or modified functionality regarding supported file '
            'formats, including support for a new file format.'
        ),
    ),
    'metadata': t_(
        'ui.tooltip.categories.metadata',
        (
            'The plugin modifies the metadata for an album or track, and is typically executed '
            'when the information is retrieved from MusicBrainz when an album is loaded.'
        ),
    ),
    'other': t_(
        'ui.tooltip.categories.other',
        (
            'The plugin provides functionality not covered by the other specific categories, or in addition '
            'to that provided by other categories.'
        ),
    ),
    'scripting': t_(
        'ui.tooltip.categories.scripting',
        (
            'The plugin provides scripting functionality, such as new script functions or new tags/variables '
            '(perhaps added via a metadata processor).'
        ),
    ),
    'ui': t_(
        'ui.tooltip.categories.ui',
        (
            'The plugin provides user interface modifications, such as new main or context menu actions, or '
            'other display modifications.'
        ),
    ),
}
