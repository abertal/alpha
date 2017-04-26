from django.db import models
from django.db.models import Value as V
from django.db.models import Q
from django.db.models.functions import Concat
from django.utils.translation import ugettext_lazy as _

import django_filters

from core.models import Group, Project


class PersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(
        label=_('Nombre'), name='name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.annotate(
            full_name=Concat('name', V(' '), 'surname',
                             output_field=models.TextField())).filter(Q(full_name__icontains=value))


class FromPersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(
        label=_('Nombre'), name='person__name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.annotate(
            full_name=Concat('person__name', V(' '), 'person__surname',
                             output_field=models.TextField())).filter(Q(full_name__icontains=value))


class GroupFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='group_name', method='custom_filter')

    class Meta:
        model = Group
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(group_name__icontains=value))


class ProjectFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='project_name', method='custom_filter')

    class Meta:
        model = Project
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(group_name__icontains=value))
