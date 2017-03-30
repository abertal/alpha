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
    id_photocopy = models.TextField(
        verbose_name='Fotocopia DNI/NIE', blank=True, default='')
    ss_number = models.TextField(
        verbose_name='Tarjeta sanitaria', blank=True, default='')
    ss_photocopy = models.TextField(
        verbose_name='Fotocopia Seguridad Social', blank=True, default='')
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
    mobile_number = models.TextField(
        verbose_name='Teléfono móvil', blank=True, default='')
    email = models.EmailField(
        verbose_name='Correo electrónico', blank=True, default='')
    dpa_authorization = models.TextField(verbose_name='LOPD', blank=True, default='')
    comment = models.TextField(
        verbose_name='Observaciones', blank=True, default='')
    health_warnings = models.TextField(
        verbose_name='Observaciones médicas', blank=True, default='')

    @property
    def age(self):
        return timesince(self.birthday) if self.birthday else None

    def __str__(self):
        return '{} {}'.format(self.name.capitalize(), self.surname.upper())


class Recipient(models.Model):
    """"Destinatario de las actividades de la asociación.

    Jóvenes asignados a un grupo dentro de un proyecto (destinatario). Pueden
    ser infantiles (6 a 14 años) o juveniles (14 a 29 años).
    """
    class Meta:
        verbose_name = 'Destinatario'

    CATEGORIES = [
        ('child', 'Infantil'),
        ('juvenile', 'Juvenil'),
    ]

    category = models.CharField('Tipo', choices=CATEGORIES, max_length=32)
    person = models.ForeignKey(Person)

    def __str__(self):
        return '{}'.format(self.id)


class Volunteer(models.Model):
    """Voluntarios, en general animadores con una vinculación con cierto plazo."""
    class Meta:
        verbose_name = 'Voluntario'
    lack_of_sexual_offenses_date_certificate = models.DateField(
        verbose_name='Fecha de emisión del Certificado de Delitos de Naturaleza Sexual',
        null=True,
        default=None,
    )
    person = models.ForeignKey(Person)

    def __str__(self):
        return '{} ({})'.format(self.id, self.person)


class Custodian(models.Model):
    """Padre, madre o tutor legal de un menor."""
    class Meta:
        verbose_name = 'Padre, madre, tutor'
    authorized_signature = models.TextField(verbose_name='Firma autorización', blank=True, default='')
    emergency_contact = models.TextField(verbose_name='Contacto de emergencia', blank=True, default='')
    CATEGORIES = [
        ('father', 'Padre'),
        ('mother', 'Madre'),
        ('legal', 'Tutor'),
    ]

    category = models.CharField('Tipo', choices=CATEGORIES, max_length=32)
    person = models.ForeignKey(Person)
    minor = models.ForeignKey(Recipient)

    def __str__(self):
        return '{}'.format(self.id)


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
    """Membresía."""
    class Meta:
        verbose_name = 'Membresía'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type_of_membership = models.TextField(verbose_name='Modalidad', blank=True, default='')

    payment_status = models.TextField(verbose_name='Estado del pago', blank=True, default='')

    membership_fee = models.DecimalField(
        verbose_name='Cuota de membresia',
        decimal_places=2,
        max_digits=6,
    )

    membership_status = models.TextField(verbose_name='Estado de socio', blank=True, default='')


class Member(models.Model):
    """Socio."""
    class Meta:
        verbose_name = 'Socio'

    CATEGORY = [
        ('child', 'Infantil'),
        ('juvenile', 'Juvenil'),
        ('volunteer', 'Voluntario'),
        ('contributor', 'Colaborador'),
        ('family', 'Familiar'),
    ]
    category = models.CharField('Tipo de socio', choices=CATEGORY, max_length=32)

    # Documentation
    id_card_status = models.TextField(verbose_name='DNI/NIE', blank=True, default='')
    ss_card_status = models.TextField(verbose_name='Tarjeta sanitaria', blank=True, default='')
    photo_status = models.TextField(verbose_name='Foto', blank=True, default='')
    dpa_status = models.TextField(verbose_name='LOPD', blank=True, default='')
    card_status = models.TextField(verbose_name='Estado del carnet', blank=True, default='')

    photo = models.ImageField(verbose_name='Fotografía', upload_to='members', default=None)

    person = models.ForeignKey(Person)
    membership = models.ForeignKey(Membership)

    @property
    def documentation_correct(self):
        return 'no' in [self.id_card_status, self.ss_card_status, self.photo_status, self.dpa_status]

    def __str__(self):
        return '{}'.format(self.id)
