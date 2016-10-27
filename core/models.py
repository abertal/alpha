from django.db import models


class Person(models.Model):
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

    def __str__(self):
        return '{} {}'.format(self.name.capitalize(), self.surname.upper())
