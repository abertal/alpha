from django.db.models import Q

import django_filters

from core.models import Group, Member, Person, Recipient, Volunteer


class PersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='name', method='custom_filter')

    class Meta:
        model = Person
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(surname__icontains=value))


class VolunteerFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name="person__name", method='custom_filter')

    class Meta:
        model = Volunteer
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class RecipientFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='person__name', method='custom_filter')

    class Meta:
        model = Recipient
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class MemberFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='person__name', method='custom_filter')

    class Meta:
        model = Member
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class GroupFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='group__name', method='custom_filter')

    class Meta:
        model = Group
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(group__name__icontains=value))
