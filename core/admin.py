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


@admin.register(models.Volunteer)
class Volunteer(admin.ModelAdmin):
    search_fields = ['person__name', 'person__surname']

    list_display = ('id',
                    'Nombre',
                    'Apellidos',
                    'lack_of_sexual_offenses_date_certificate',)

    def Nombre(self, obj):
        return obj.person.name

    def Apellidos(self, obj):
        return obj.person.surname


@admin.register(models.Custodian)
class Custodian(admin.ModelAdmin):
    search_fields = ['person__name', 'person__surname']

    list_display = ('id',
                    'category',
                    'person',
                    'minor')


@admin.register(models.Project)
class Project(admin.ModelAdmin):
    search_fields = ['project_name']

    list_display = ('id', 'project_name')


@admin.register(models.Group)
class Group(admin.ModelAdmin):
    search_fields = ['group_name', 'project']

    list_display = ('id', 'group_name')


@admin.register(models.Event)
class Event(admin.ModelAdmin):
    search_fields = ['event_name']

    list_display = ('id', 'event_name')


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


@admin.register(models.Member)
class Member(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'person',
        'membership',
        'id_card_status',
        'ss_card_status',
        'photo_status',
        'dpa_status',
        'card_status',
        'photo'
    )
