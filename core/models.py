from django.db import models


class Person(models.Model):
    name = models.TextField(verbose_name='Nombre')
    surname = models.TextField(verbose_name='Apellidos')
    birthday = models.DateField(verbose_name='Fecha de nacimiento')
    id_number = models.TextField(verbose_name='DNI/NIE')
    ss_number = models.TextField(verbose_name='Tarjeta sanitaria')
    address_street = models.TextField(verbose_name='Dirección')
    address_locality = models.TextField(verbose_name='Localidad')
    address_region = models.TextField(verbose_name='Provincia')
    address_country = models.TextField(verbose_name='País')
    phone_number = models.TextField(verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Correo electrónico')
    comment = models.TextField(verbose_name='Observaciones')
    health_warnings = models.TextField(verbose_name='Observaciones médicas')
