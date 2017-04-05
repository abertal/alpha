import django_filters

from core.models import Person, Volunteer


class PersonFilter(django_filters.FilterSet):

    class Meta:
        model = Person
        fields = ['name']


class VolunteerFilter(django_filters.FilterSet):

    class Meta:
        model = Volunteer
        fields = ['person__name']
