import pytest

from webapp import forms


@pytest.mark.django_db
def test_success(recipient, person):
    data = {'minor': recipient.pk, 'person': person.pk, 'category': 'mother'}
    form = forms.CreateCustodian(data=data)
    assert form.is_valid(), form.errors
    custodian = form.save()
    assert custodian in recipient.custodian_set.all()
