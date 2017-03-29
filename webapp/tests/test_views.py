from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import reverse
from django.test import Client

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('view_name', [
    'person-list',
    'missing_doc',
])
def test_list_views(logged_client, view_name):
    url = reverse(view_name)
    response = logged_client.get(url)
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
def test_views_exist(logged_client, url):
    response = logged_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/login/',
])
def test_views_post_and_redirect(url):
    c = Client()
    User.objects.create_user('user00', 'first.last@example.com', 'secret')
    response = c.post(url, {'user': 'user00', 'password': 'secret'})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/login/',
])
def test_login_incorrect(url):
    c = Client()
    response = c.post(url, {'user': 'user00', 'password': 'secret1'})
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/basicformnewperson/',
    '/webapp/basicformnewfamily/',
])
def test_views_post_with_errors(logged_client, url):
    response = logged_client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/{}/',
    '/webapp/person/{}/edit/',
])
def test_person_views(logged_client, person, url):
    response = logged_client.get(url.format(person.id))
    assert response.status_code == 200
