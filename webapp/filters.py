from django.db.models import Q

import django_filters

from core.models import Member, Person, Recipient, Volunteer


class PersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='name', method='custom_filter')

    class Meta:
        model = Person
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(surname__icontains=value))


class VolunteerFilter(django_filters.FilterSet):

    class Meta:
        model = Volunteer
        fields = ['person__name']


class RecipientFilter(django_filters.FilterSet):

    class Meta:
        model = Recipient
        fields = ['person__name']


class MemberFilter(django_filters.FilterSet):

    class Meta:
        model = Member
        fields = ['person__name']
