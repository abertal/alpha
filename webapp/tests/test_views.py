from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('view_name', [
    'member-list',
    'person-list',
    'recipient-list',
    'volunteer-list',
    'missing_doc',
])
def test_list_views(logged_client, view_name):
    url = reverse(view_name)
    response = logged_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
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
def test_check_user(logged_client, url):
    data = {'username': 'user00', 'password': 'secret'}
    response = logged_client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/new/',
])
def test_create_person(logged_client, url):
    data = {'name': 'Juan', 'surname': 'Bosco'}
    response = logged_client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/{}/edit/',
])
def test_edit_person(logged_client, person, url):
    data = {'name': 'Juan', 'surname': 'Bosco'}
    response = logged_client.post(url.format(person.id), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/{}/delete/',
])
def test_delete_person(logged_client, person, url):
    data = {'name': 'Juan', 'surname': 'Bosco'}
    response = logged_client.post(url.format(person.id), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/{}/delete/',
])
def test_wrong_delete_person(logged_client, volunteer_filter, url):
    response = logged_client.post(url.format(
        volunteer_filter.person.id), {'name': volunteer_filter.person.name})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url, data', [
    ('/webapp/person/{pk}/volunteer/', {}),
    ('/webapp/person/{pk}/recipient/', {}),
])
def test_create_from_person(logged_client, person, url, data):
    # Inject person UID to POST data
    data['person'] = person.pk
    response = logged_client.post(url.format(pk=person.id), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/login/',
])
def test_views_post_and_redirect(url):
    c = Client()
    User.objects.create_user('user00', 'first.last@example.com', 'secret')
    response = c.post(url, {'username': 'user00', 'password': 'secret'})
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
    '/webapp/person/new/',
    '/webapp/basicformnewperson/',
    '/webapp/basicformnewfamily/',
])
def test_views_post_with_errors(logged_client, url):
    response = logged_client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/logout'
])
def test_user_logged_out(logged_client, url):
    response = logged_client.get(url, follow=True)
    assert not response.context['user'].is_authenticated


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/person/{}/',
    '/webapp/person/{}/edit/',
    '/webapp/person/{}/volunteer/',
])
def test_person_views(logged_client, person, url):
    response = logged_client.get(url.format(person.id))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/group/{pk}/edit/',
])
def test_edit_group(logged_client, group_filter, url):
    response = logged_client.post(url.format(pk=group_filter.id), {'group_name': 'group_name'})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/recipient/{pk}/edit/',
])
def test_edit_recipient(logged_client, recipient_filter, url):
    response = logged_client.post(url.format(pk=recipient_filter.id), {'category': 'child'})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/volunteer/{pk}/edit/',
])
def test_edit_volunteer(logged_client, volunteer_filter, url):
    response = logged_client.post(url.format(pk=volunteer_filter.id),
                                  {'lack_of_sexual_offenses_date_certificate': '23/03/2017'})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/webapp/volunteer/{pk}/',
])
def test_detail_volunteer(logged_client, volunteer_filter, url):
    response = logged_client.get(url.format(pk=volunteer_filter.id))
    assert response.status_code == 200
