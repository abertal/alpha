import pytest

from webapp import forms


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

    membership = form.execute()
    assert membership.pk is not None
