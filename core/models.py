from django.db import models
from django.template.defaultfilters import timesince


class Person(models.Model):
    class Meta:
        verbose_name = 'Persona'

    name = models.TextField(verbose_name='Nombre')
    surname = models.TextField(verbose_name='Apellidos')
    birthday = models.DateField(verbose_name='Fecha de nacimiento', blank=True, null=True)
    id_number = models.TextField(verbose_name='DNI/NIE', blank=True, default='')
    ss_number = models.TextField(verbose_name='Tarjeta sanitaria', blank=True, default='')
    address_street = models.TextField(verbose_name='Dirección', blank=True, default='')
    address_locality = models.TextField(verbose_name='Localidad', blank=True, default='')
    address_region = models.TextField(verbose_name='Provincia', blank=True, default='')
    address_country = models.TextField(verbose_name='País', blank=True, default='')
    phone_number = models.TextField(verbose_name='Teléfono', blank=True, default='')
    email = models.EmailField(verbose_name='Correo electrónico', blank=True, default='')
    comment = models.TextField(verbose_name='Observaciones', blank=True, default='')
    health_warnings = models.TextField(verbose_name='Observaciones médicas', blank=True, default='')

    @property
    def age(self):
        return timesince(self.birthday)

    def __str__(self):
        return '{} {}'.format(self.name.capitalize(), self.surname.upper())


class Group(models.Model):
    class Meta:
        verbose_name = 'Grupo'

    group_name = models.TextField(verbose_name='Nombre grupo')

    def __str__(self):
        return self.group_name


class Enrolment(models.Model):
    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = (('person', 'group'),)

    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
