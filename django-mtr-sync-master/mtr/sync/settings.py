import os

from django.conf import settings as dsettings

from mtr.utils.settings import getattr_with_prefix, strip_media_root


def get_buffer_file_path(instance, filename, absolute=False):
    """Generate file path for report"""

    action = getattr(instance, 'action', 1)
    action = 'import' if action else 'export'
    path = os.path.join(
        dsettings.MEDIA_ROOT, 'sync', action, filename.lower())

    if not absolute:
        path = strip_media_root(path)

    return path

SETTINGS = getattr_with_prefix('SYNC', 'SETTINGS', {
    'path': get_buffer_file_path,
    'default_processor': 'XlsxProcessor',
    'actions': ['mtr.sync.lib.actions'],
    'converters': ['mtr.sync.lib.converters'],
    'processors': [
        'mtr.sync.lib.processors.xlsx',
        'mtr.sync.lib.processors.xls',
        'mtr.sync.lib.processors.ods',
        'mtr.sync.lib.processors.csv',
    ],
    'broker': 'rq',
    'include': {
        'api': False,
        'admin': True,
    }
})
