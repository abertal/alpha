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


@admin.register(models.Enrolment)
class Enrolment(admin.ModelAdmin):
    search_fields = ['group', 'person']

    list_display = ('group', 'person', 'created')


@admin.register(models.Membership)
class Membership(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'surname', 'role', 'group', 'phone_number',
                    'mobile_number', 'email', 'id_card', 'ss_card', 'photo', 'DPA', 'membership_fee',
                    'membership_payment', 'done_idmembership', 'delivered_idmembership')
