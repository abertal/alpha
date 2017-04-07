from django.test import TransactionTestCase

import pytest
from django_filters import Filter

from core.models import Member, Membership, Person, Recipient, Volunteer
from webapp.filters import MemberFilter, PersonFilter, RecipientFilter, VolunteerFilter
from webapp.tests.conftest import person_filter


class FilterTests(TransactionTestCase):

    @pytest.mark.django_db
    def test_filtering(self):
        t = TransactionTestCase()
        person_filter()
        qs = Person.objects.all().order_by('name')
        f = Filter(name='name', lookup_expr='icontains')
        result = f.filter(qs, 'ex')
        qs2 = PersonFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_volunteer(self):
        t = TransactionTestCase()
        p1 = Person(name='Example')
        p1.save()
        v1 = Volunteer(person=p1)
        v1.save()
        qs = Volunteer.objects.all().order_by('id')
        f = Filter(name='person__name', lookup_expr='icontains')
        result = f.filter(qs, 'ex')
        qs2 = VolunteerFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_recipient(self):
        t = TransactionTestCase()
        p1 = Person(name='Example')
        p1.save()
        r1 = Recipient(person=p1)
        r1.save()
        qs = Recipient.objects.all().order_by('id')
        f = Filter(name='person__name', lookup_expr='icontains')
        result = f.filter(qs, 'ex')
        qs2 = RecipientFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_member(self):
        t = TransactionTestCase()
        p1 = Person(name='Example')
        p1.save()
        mship = Membership(membership_fee=2)
        mship.save()
        m1 = Member(person=p1, membership=mship)
        m1.save()
        qs = Member.objects.all().order_by('id')
        f = Filter(name='person__name', lookup_expr='icontains')
        result = f.filter(qs, 'ex')
        qs2 = MemberFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])
