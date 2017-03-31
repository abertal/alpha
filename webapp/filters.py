import django_filters

from core.models import Person


# Create your models here.


class PersonFilter(django_filters.FilterSet):

    class Meta:
        model = Person
        fields = ['name']
