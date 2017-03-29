from django.contrib.auth.models import User
from django.test import Client

import pytest

from core import models


@pytest.fixture
def person():
    return models.Person.objects.create(name='Juan', surname='Bosco')


@pytest.fixture
def logged_client():
    c = Client()
    user = User.objects.create_user('user00', 'first.last@example.com', 'secret')
    c.force_login(user)
    return c
