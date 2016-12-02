from django.conf.urls import url

from .settings import SETTINGS

if SETTINGS['include']['api']:
    from .api import SettingsAPI, FieldAPI

    urlpatterns = (
        url(r'^api/settings', SettingsAPI.as_view()),
        url(r'^api/fields', FieldAPI.as_view())
    )
