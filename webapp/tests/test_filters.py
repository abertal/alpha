from django.test import TransactionTestCase

import pytest

import webapp.tests.conftest as fixture
from webapp.filters import MemberFilter, PersonFilter, RecipientFilter, VolunteerFilter


class FilterTests(TransactionTestCase):

    @pytest.mark.django_db
    def test_filtering(self):
        t = TransactionTestCase()
        qs = fixture.person_query_filter()
        result = fixture.filter_name().filter(qs, 'ex')
        qs2 = PersonFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_volunteer(self):
        t = TransactionTestCase()
        qs = fixture.volunteer_query_filter()
        result = fixture.filter_person_name().filter(qs, 'ex')
        qs2 = VolunteerFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_recipient(self):
        t = TransactionTestCase()
        qs = fixture.recipient_query_filter()
        result = fixture.filter_person_name().filter(qs, 'ex')
        qs2 = RecipientFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_member(self):
        t = TransactionTestCase()
        qs = fixture.member_query_filter()
        result = fixture.filter_person_name().filter(qs, 'ex')
        qs2 = MemberFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])
