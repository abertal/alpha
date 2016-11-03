from django.contrib import admin

from . import models


@admin.register(models.Person)
@admin.register(models.Group)
class Person(admin.ModelAdmin):
    search_fields = ['name', 'surname']

    list_display = ('id',
                    'name',
                    'surname',
                    'phone_number',
                    'birthday',
                    'age')
