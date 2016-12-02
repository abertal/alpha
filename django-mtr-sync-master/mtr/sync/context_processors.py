from .models import Settings


def settings_global():
    return Settings.objects.filter(show_in_quick_menu=True)


def settings(request):
    return {'mtr': {'sync': {
        'settings': settings_global
    }}}
