from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('view_name', [
    'person-list',
    'missing_doc',
])
def test_list_views(view_name):
    url = reverse(view_name)
    c = Client()
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/login/',
    '/webapp/home/',
    '/webapp/membership/',
    '/webapp/basicformnewperson/',
    '/webapp/basicformnewfamily/',
    '/webapp/person/',
])
def test_views_exist(url):
    c = Client()
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/login/',
])
def test_views_post_and_redirect(url):
    c = Client()
    user = User.objects.create_user('user00', 'first.last@example', 'secret')
    response = c.post(url, {'user': 'user00', 'password': 'secret'})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/basicformnewperson/',
    '/webapp/basicformnewfamily/',
])
def test_views_post_with_errors(url):
    c = Client()
    response = c.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/{}/',
    '/webapp/person/{}/edit/',
])
def test_person_views(person, url):
    c = Client()
    response = c.get(url.format(person.id))
    assert response.status_code == 200
