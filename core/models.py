import uuid

from django.db import models
from django.template.defaultfilters import timesince
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):

    class Meta:
        verbose_name = _('Persona')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.TextField(verbose_name=_('Nombre'))
    surname = models.TextField(verbose_name=_('Apellidos'))
    birthday = models.DateField(
        verbose_name=_('Fecha de nacimiento'), blank=True, null=True)
    id_number = models.TextField(
        verbose_name=_('DNI/NIE'), blank=True, default='')
    id_photocopy = models.TextField(
        verbose_name=_('Fotocopia DNI/NIE'), blank=True, default='')
    ss_number = models.TextField(
        verbose_name=_('Tarjeta sanitaria'), blank=True, default='')
    ss_photocopy = models.TextField(
        verbose_name=_('Fotocopia Seguridad Social'), blank=True, default='')
    postal_code = models.TextField(
        verbose_name=_('Código postal'), blank=True, default='')
    address_street = models.TextField(
        verbose_name=_('Dirección'), blank=True, default='')
    address_locality = models.TextField(
        verbose_name=_('Localidad'), blank=True, default='')
    address_region = models.TextField(
        verbose_name=_('Provincia'), blank=True, default='')
    address_country = models.TextField(
        verbose_name=_('País'), blank=True, default='')
    phone_number = models.TextField(
        verbose_name=_('Teléfono'), blank=True, default='')
    mobile_number = models.TextField(
        verbose_name=_('Teléfono móvil'), blank=True, default='')
    email = models.EmailField(
        verbose_name=_('Correo electrónico'), blank=True, default='')
    dpa_authorization = models.TextField(verbose_name=_('LOPD'), blank=True, default='')
    comment = models.TextField(
        verbose_name=_('Observaciones'), blank=True, default='')
    health_warnings = models.TextField(
        verbose_name=_('Observaciones médicas'), blank=True, default='')

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
        verbose_name = _('Destinatario')

    CATEGORIES = [
        ('child', _('Infantil')),
        ('juvenile', _('Juvenil')),
    ]
    estudies = models.TextField(
        verbose_name=_('Estudios'), blank=True, default='')
    brother_sister = models.IntegerField(
        verbose_name=_('Hermanos'), blank=True, default='')
    Authorize_photo = models.TextField(
        verbose_name=_('Autoriza foto'), blank=True, default='')
    category = models.CharField(_('Tipo'), choices=CATEGORIES, max_length=32)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.id)


class Volunteer(models.Model):
    """Voluntarios, en general animadores con una vinculación con cierto plazo."""
    class Meta:
        verbose_name = _('Voluntario')
    lack_of_sexual_offenses_date_certificate = models.DateField(
        verbose_name='Fecha de emisión del Certificado de Delitos de Naturaleza Sexual',
        null=True,
        default=None,
    )
    comment = models.TextField(
        verbose_name=_('Observaciones'), blank=True, default='')
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

    def __str__(self):
        return '{} ({})'.format(self.id, self.person)


class Custodian(models.Model):
    """Padre, madre o tutor legal de un menor."""
    class Meta:
        verbose_name = _('Padre, madre, tutor')
    authorized_signature = models.TextField(verbose_name=_('Firma autorización'), blank=True, default='')
    emergency_contact = models.TextField(verbose_name=_('Contacto de emergencia'), blank=True, default='')
    CATEGORIES = [
        ('father', _('Padre')),
        ('mother', _('Madre')),
        ('legal', _('Tutor')),
    ]

    category = models.CharField(_('Tipo'), choices=CATEGORIES, max_length=32)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    minor = models.ForeignKey(Recipient, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.id)


class Group(models.Model):

    class Meta:
        verbose_name = _('Grupo')

    group_name = models.TextField(verbose_name=_('Nombre grupo'))

    def __str__(self):
        return '{}'.format(self.id)


class Enrolment(models.Model):

    class Meta:
        verbose_name = _('Inscripción')
        verbose_name_plural = _('Inscripciones')
        unique_together = (('person', 'group'),)

    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Fecha de inscripción'))


class Membership(models.Model):
    """Membresía."""
    class Meta:
        verbose_name = _('Membresía')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type_of_membership = models.TextField(verbose_name=_('Modalidad'), blank=True, default='')

    payment_status = models.TextField(verbose_name=_('Estado del pago'), blank=True, default='')

    membership_fee = models.DecimalField(
        verbose_name=_('Cuota de membresia'),
        decimal_places=2,
        max_digits=6,
    )

    membership_status = models.TextField(verbose_name=_('Estado de socio'), blank=True, default='')


class Member(models.Model):
    """Socio."""
    class Meta:
        verbose_name = _('Socio')

    CATEGORY = [
        ('child', _('Infantil')),
        ('juvenile', _('Juvenil')),
        ('volunteer', _('Voluntario')),
        ('contributor', _('Colaborador')),
        ('family', _('Familiar')),
    ]
    category = models.CharField(_('Tipo de socio'), choices=CATEGORY, max_length=32)

    # Documentation
    id_card_status = models.TextField(verbose_name=_('DNI/NIE'), blank=True, default='')
    ss_card_status = models.TextField(verbose_name=_('Tarjeta sanitaria'), blank=True, default='')
    photo_status = models.TextField(verbose_name=_('Foto'), blank=True, default='')
    dpa_status = models.TextField(verbose_name=_('LOPD'), blank=True, default='')
    card_status = models.TextField(verbose_name=_('Estado del carnet'), blank=True, default='')
    bursary = model.TextField(verbose_name=_('Beca'), blank=True, default='')
    photo = models.ImageField(verbose_name=_('Fotografía'), upload_to='members', blank=True, null=True)

    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)

    @property
    def documentation_correct(self):
        return 'no' in [self.id_card_status, self.ss_card_status, self.photo_status, self.dpa_status]

    def __str__(self):
        return '{}'.format(self.id)
