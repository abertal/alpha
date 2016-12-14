import uuid

from django.db import models
from django.template.defaultfilters import timesince


class Person(models.Model):

    class Meta:
        verbose_name = 'Persona'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.TextField(verbose_name='Nombre')
    surname = models.TextField(verbose_name='Apellidos')
    birthday = models.DateField(
        verbose_name='Fecha de nacimiento', blank=True, null=True)
    id_number = models.TextField(
        verbose_name='DNI/NIE', blank=True, default='')
    ss_number = models.TextField(
        verbose_name='Tarjeta sanitaria', blank=True, default='')
    address_street = models.TextField(
        verbose_name='Dirección', blank=True, default='')
    address_locality = models.TextField(
        verbose_name='Localidad', blank=True, default='')
    address_region = models.TextField(
        verbose_name='Provincia', blank=True, default='')
    address_country = models.TextField(
        verbose_name='País', blank=True, default='')
    phone_number = models.TextField(
        verbose_name='Teléfono', blank=True, default='')
    email = models.EmailField(
        verbose_name='Correo electrónico', blank=True, default='')
    comment = models.TextField(
        verbose_name='Observaciones', blank=True, default='')
    health_warnings = models.TextField(
        verbose_name='Observaciones médicas', blank=True, default='')

    @property
    def age(self):
        return timesince(self.birthday) if self.birthday else None

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

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de inscripción')

class Membership(models.Model):

    class Meta:
        verbose_name = 'Membresia'

    id = models.TextField(primary_key=True, default='', editable=False)

    uuid = models.TextField(verbose_name='id Membresia', blank=True, default='')
    name = models.TextField(verbose_name='Nombre', blank=True, default='')
    surname = models.TextField(verbose_name='Apellidos', blank=True, default='')
    role = models.TextField(verbose_name='Rol', blank=True, default='')
    group = models.TextField(verbose_name='Grupo', blank=True, default='')
    phone_number = models.TextField(verbose_name='Teléfono', blank=True, default='')
    mobile_number = models.TextField(verbose_name='Movil', blank=True, default='')
    email = models.TextField(verbose_name='email', blank=True, default='')
    id_card = models.TextField(verbose_name='DNI/NIE', blank=True, default='')
    ss_card = models.TextField(verbose_name='Tarjeta sanitaria', blank=True, default='')
    photo = models.TextField(verbose_name='Foto', blank='True', default='')
    DPA = models.TextField(verbose_name='LOPD', blank=True, default='')
    membership_fee = models.TextField(verbose_name='Cuota de membresia', blank=True, default='')
    membership_payment = models.TextField(verbose_name='Pago de membresia', blank=True, default='')
    done_idmembership = models.TextField(verbose_name='Carnet para entregar', blank=True, default='')
    delivered_idmembership = models.TextField(verbose_name='Carnet entragado', blank=True, default='')
