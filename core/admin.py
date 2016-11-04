from django.contrib import admin

from . import models


@admin.register(models.Person)
class Person(admin.ModelAdmin):
    search_fields = ['name', 'surname']

    list_display = ('id',
                    'name',
                    'surname',
                    'phone_number',
                    'birthday',
                    'age')


@admin.register(models.Group)
class Group(admin.ModelAdmin):
    search_fields = ['group_name']

    list_display = ('id', 'group_name')

@admin.register(models.PersonGroup)
class PersonGroup(admin.ModelAdmin):
    search_fields = ['group', 'person']

    list_display = ('group', 'person')
