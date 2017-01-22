import os.path
from io import StringIO

from django.core.management import call_command

import pytest


@pytest.mark.django_db
def test_command_output():
    out = StringIO()
    filename = os.path.join(os.path.dirname(__file__), 'maestro.xlsx')
    call_command('importdata', filename, stdout=out)
    assert 'Importación finalizada con éxito.' in out.getvalue()
