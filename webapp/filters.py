from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

import django_filters


class PersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(surname__icontains=value))


class VolunteerFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class RecipientFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class MemberFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class GroupFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='group_name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(group_name__icontains=value))
