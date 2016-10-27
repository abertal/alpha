from django.contrib import admin

from . import models


@admin.register(models.Person)
class Person(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'surname',
                    'phone_number',
                    'birthday',)
