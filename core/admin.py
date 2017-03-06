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


@admin.register(models.Recipient)
class Recipient(admin.ModelAdmin):
    search_fields = ['person__name', 'person__surname']

    list_display = ('id',
                    'category')


@admin.register(models.Group)
class Group(admin.ModelAdmin):
    search_fields = ['group_name']

    list_display = ('id', 'group_name')


@admin.register(models.Enrolment)
class Enrolment(admin.ModelAdmin):
    search_fields = ['group', 'person']

    list_display = ('group', 'person', 'created')


@admin.register(models.Membership)
class Membership(admin.ModelAdmin):
    list_display = (
        'id',
        'membership_status',
        'payment_status',
        'membership_fee',
    )


@admin.register(models.PersonMembership)
class PersonMembership(admin.ModelAdmin):
    list_display = (
        'id',
        'person',
        'id_card_status',
        'ss_card_status',
        'photo_status',
        'dpa_status',
        'card_status',
    )
