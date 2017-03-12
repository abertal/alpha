import pytest

from core import models


@pytest.fixture
def person():
    return models.Person.objects.create(name='Juan', surname='Bosco')
