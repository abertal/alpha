import pytest

from core import models


@pytest.mark.parametrize('filename, ext', [
    ('image.png', '.png'),
    ('noext', ''),
])
def test_get_file_path(filename, ext):
    new_filename = models._get_file_path(None, filename)
    assert new_filename.endswith(f'{ext}')
