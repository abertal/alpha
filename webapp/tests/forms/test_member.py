from decimal import Decimal as D

import pytest

from webapp import forms


@pytest.mark.django_db
def test_create(person):
    data = {'person': person.id, 'membership_fee': D('0')}
    form = forms.MemberCreate(data=data)
    assert form.is_valid()
    member = form.save()
    assert member.person == person
