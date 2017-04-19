from django.test import TransactionTestCase

import pytest

import webapp.tests.conftest as fixture
from webapp.filters import FromPersonFilter, GroupFilter, PersonFilter


class FilterTests(TransactionTestCase):

    @pytest.mark.django_db
    def test_filtering(self):
        t = TransactionTestCase()
        qs = fixture.person_query_filter()
        result = fixture.filter_name().filter(qs, 'ex')
        qs2 = PersonFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])

    def test_filter_from_person(self):
        t = TransactionTestCase()
        qs = fixture.from_person_query_filter()
        result = fixture.filter_person_name().filter(qs, 'ex')
        qs2 = FromPersonFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])
    
    def test_filter_group(self):
        t = TransactionTestCase()
        qs = fixture.group_query_filter()
        result = fixture.filter_group_name().filter(qs, 'ex')
        qs2 = GroupFilter.custom_filter(self, qs, '', 'ex')
        t.assertQuerysetEqual(qs2, [repr(r) for r in result])
