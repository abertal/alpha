from django.forms.models import model_to_dict

import pytest

from core import models
from webapp import forms, views


@pytest.mark.django_db
def test_create_person_form():
    data = {'name': 'John', 'surname': 'Bosco'}
    form = forms.CreatePerson(data)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert obj.name == 'John'


@pytest.mark.django_db
def test_edit_person_form(person):
    data = model_to_dict(person)
    data['name'] = 'John'
    form = forms.EditPerson(data, instance=person)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert obj.name == 'John'


@pytest.mark.django_db
def test_create_recipient_form(person):
    data = {'person': person.id}
    form = forms.RecipientCreate(data)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert obj.person.name == 'Juan'
    assert str(obj) == '{}'.format(obj.id)


@pytest.mark.django_db
def test_create_custodian_form(person):
    data = {'person': person.id}
    form = forms.RecipientCreate(data)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert obj.person.name == 'Juan'
    assert str(obj) == '{}'.format(obj.id)


@pytest.mark.django_db
def test_create_volunteer_form(person):
    data = {'person': person.id}
    form = forms.VolunteerCreate(data)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert obj.person.id == person.id


@pytest.mark.django_db
def test_new_individual_member():
    data = {
        'mail': 'email@example.com',
        'surname': 'García',
        'adress': 'Gran Vía',
        'phone': '555555555',
        'name': 'Juan',
        'id_number': '12345678A'
    }
    form = forms.NewIndividualMember(data=data)
    assert form.is_valid(), form.errors
    view = views.NewIndividualMember
    response = view.form_valid(None, form)
    assert response.status_code == 302
    membership = form.execute()
    assert membership.pk is not None
    assert isinstance(membership, models.Membership)


@pytest.mark.django_db
def test_new_family_member():
    data = {
        'name1': 'Juan',
        'phone1': '555555555',
        'surname1': 'García',
        'id_number1': '12345678A',
        'mail1': 'email@example.com',

        'name2': 'Juan',
        'phone2': '555555555',
        'surname2': 'García',
        'id_number2': '12345678A',
        'mail2': 'email@example.com',

        'name3': 'Juan',
        'phone3': '555555555',
        'surname3': 'García',
        'id_number3': '12345678A',
        'mail3': 'email@example.com',

        'name4': 'Juan',
        'phone4': '555555555',
        'surname4': 'García',
        'id_number4': '12345678A',
        'mail4': 'email@example.com',
    }
    form = forms.NewFamilyMember(data=data)
    assert form.is_valid(), form.errors
    view = views.NewFamilyMember
    response = view.form_valid(None, form)
    assert response.status_code == 302
    membership = form.execute()
    assert membership.pk is not None
    assert isinstance(membership, models.Membership)
