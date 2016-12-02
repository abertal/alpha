from django.apps import AppConfig

from .translation import gettext_lazy as _


class MtrSyncConfig(AppConfig):
    name = 'mtr.sync'
    label = 'mtr_sync'
    verbose_name = _('Data sync')
