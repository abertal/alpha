from decimal import Decimal as D

from django.contrib.auth.models import User
from django.test import Client

import pytest
from django_filters import Filter

from core import models


@pytest.fixture
def person():
    return models.Person.objects.create(name='Juan', surname='Bosco')


@pytest.fixture
def recipient():
    return models.Recipient.objects.create(
        person=models.Person.objects.create(name='Name_example', surname='Surname_example'))


@pytest.fixture
def custodian():
    return models.Custodian.objects.create(person=person(), minor=recipient())


@pytest.fixture
def membership():
    return models.Membership.objects.create(membership_fee=D('15.00'))


@pytest.fixture
def member():
    return models.Member.objects.create(person=person(), membership=membership())


@pytest.fixture
def logged_client():
    c = Client()
    user = User.objects.create_user(
        'user00', 'first.last@example.com', 'secret')
    c.force_login(user)
    return c


@pytest.fixture
def group():
    return models.Group.objects.create(group_name='Example group')


@pytest.fixture
def person_filter():
    return models.Person.objects.create(name='Example', surname='SurExample')


@pytest.fixture
def person_query_filter():
    person_filter()
    return models.Person.objects.all().order_by('name')


@pytest.fixture
def volunteer_filter():
    person_filter()
    return models.Volunteer.objects.create(person=models.Person.objects.get(name='Example'))


@pytest.fixture
def from_person_query_filter():
    volunteer_filter()
    return models.Volunteer.objects.all().order_by('id')


@pytest.fixture
def filter_name():
    f = Filter(name='name', lookup_expr='icontains')
    return f


@pytest.fixture
def filter_person_name():
    f = Filter(name='person__name', lookup_expr='icontains')
    return f


@pytest.fixture
def group_filter():
    return models.Group.objects.create(group_name='Example Group')


@pytest.fixture
def filter_group_name():
    f = Filter(name='group_name', lookup_expr='icontains')
    return f


@pytest.fixture
def group_query_filter():
    group_filter()
    return models.Group.objects.all().order_by('id')
