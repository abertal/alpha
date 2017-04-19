from itertools import chain
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

import django_filters

from core.models import Group, Member, Person, Recipient, Volunteer


class PersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='name', method='custom_filter')

    class Meta:
        model = Person
        fields = []

    def custom_filter(self, queryset, name, value):
        value_array = value.split(' ', 1)
        value1 = value_array[0]
        if(len(value_array) == 2):
            value2 = value_array[1]
            surname_query = queryset.filter(Q(surname__icontains=value2))
        else:
            surname_query = []
        name_query = queryset.filter(
            Q(name__icontains=value1) | Q(surname__icontains=value1))
        for p_name in name_query:
            for p_surname in surname_query:
                if p_name.name == p_surname.name:
                    return name_query
        return list(chain(name_query, surname_query))


class VolunteerFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    class Meta:
        model = Volunteer
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class RecipientFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    class Meta:
        model = Recipient
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class MemberFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    class Meta:
        model = Member
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class GroupFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='group_name', method='custom_filter')

    class Meta:
        model = Group
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(group_name__icontains=value))
