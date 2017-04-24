from django.db.models import Q, Value as V
from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import Concat
import django_filters

from core.models import Group


class PersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        combined_name=Concat(name,V(' '),surname)
        return queryset.filter(Q(name__icontains=value)).annotate(' ').filter(Q(surname_icontains=value))


class FromPersonFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(label=_('Nombre'), name='person__name', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(person__name__icontains=value) | Q(person__surname__icontains=value))


class GroupFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(name='group_name', method='custom_filter')

    class Meta:
        model = Group
        fields = []

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(group_name__icontains=value))
