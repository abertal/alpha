from decimal import Decimal as D

from django import forms
from django.utils.text import force_text
from django.utils.translation import ugettext_lazy as _

from core import models


class Fieldset:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.fields = []


class CreatePerson(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = 'name', 'surname'

        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
        }


class EditPerson(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = (
            'name', 'surname', 'birthday', 'id_number', 'ss_number',
            'address_street', 'address_locality', 'address_region', 'address_country',
            'phone_number', 'mobile_number', 'email',
            'comment',
        )

        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
            'birthday': forms.DateInput(),
            'id_number': forms.TextInput(),
            'ss_number': forms.TextInput(),
            'address_street': forms.TextInput(),
            'address_locality': forms.TextInput(),
            'address_region': forms.TextInput(),
            'address_country': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'mobile_number': forms.TextInput(),
            'email': forms.TextInput()
        }

        wrapper_class = {
            'birthday': 'col-xs-12 col-sm-4',
            'id_number': 'col-xs-12 col-sm-4',
            'ss_number': 'col-xs-12 col-sm-4',
            'address_locality': 'col-xs-12 col-sm-4',
            'address_region': 'col-xs-12 col-sm-4',
            'address_country': 'col-xs-12 col-sm-4',
            'phone_number':  'col-xs-12 col-sm-6',
            'mobile_number': 'col-xs-12 col-sm-6',
        }

        # 'name', 'surname'
        fieldsets = [
            ('Datos personales', 1, ['birthday', 'id_number', 'ss_number']),
            ('Dirección', 2, ['address_street', 'address_locality', 'address_region', 'address_country']),
            ('Datos de contacto', 3, ['phone_number', 'mobile_number', 'email']),
            ('Observaciones', 4, ['comment'])
        ]

    def fieldsets(self):
        rv = []
        for item in self.Meta.fieldsets:
            label, index, fields = item
            fieldset = Fieldset(label, index)
            for field_name in fields:
                field = self[field_name]
                if not field.is_hidden:
                    field.wrapper_class = self.Meta.wrapper_class.get(field_name)
                    fieldset.fields.append(field)
            rv.append(fieldset)
        return rv

    def visible_fields(self):
        attached_fields = set()
        for item in self.Meta.fieldsets:
            _, index, fields = item
            attached_fields.update(fields)
        return [field for field in self if not field.is_hidden and field.name not in attached_fields]


def create_from_person_factory(model):
    """Create a form class to create model depending on check."""
    verbose_name = force_text(model._meta.verbose_name)

    class CreateFrom(forms.Form):
        create = forms.BooleanField(label='Crear %s' % verbose_name, required=False)

        def __init__(self, person, *args, **kwargs):
            self.person = person
            super().__init__(*args, **kwargs)

        def save(self):
            if self.cleaned_data['create']:
                return model.objects.create(person=self.person)

    return CreateFrom


class RecipientCreate(forms.ModelForm):
    class Meta:
        model = models.Recipient
        fields = 'person',

        widgets = {
            'person': forms.HiddenInput(),
        }


class RecipientEdit(forms.ModelForm):
    class Meta:
        model = models.Recipient
        fields = 'category', 'courses', 'school', 'sibling',
        wrapper_class = {
            'category': 'col-xs-12 col-sm-6',
            'courses': 'col-xs-12 col-sm-6',
            'school': 'col-xs-12 col-sm-6',
            'sibling': 'col-xs-12 col-sm-6',
        }

        fieldsets = [
            ('Destinatario', '', ['category', 'courses', 'school', 'sibling']),
        ]

    def fieldsets(self):
        rv = []
        for item in self.Meta.fieldsets:
            label, index, fields = item
            fieldset = Fieldset(label, index)
            for field_name in fields:
                field = self[field_name]
                if not field.is_hidden:
                    field.wrapper_class = self.Meta.wrapper_class.get(field_name)
                    fieldset.fields.append(field)
            rv.append(fieldset)
        return rv


class VolunteerCreate(forms.ModelForm):
    class Meta:
        model = models.Volunteer
        fields = 'person',

        widgets = {
            'person': forms.HiddenInput(),
        }


class VolunteerEdit(forms.ModelForm):
    class Meta:
        model = models.Volunteer
        fields = 'lack_of_sexual_offenses_date_certificate', 'comment',
        widgets = {'lack_of_sexual_offenses_date_certificate': forms.DateInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lack_of_sexual_offenses_date_certificate'].required = False


class EventCreate(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ('event_name', 'event_start', 'event_end')
        widgets = {
            'event_name': forms.TextInput(),
            'event_start': forms.DateInput(),
            'event_end': forms.DateInput(),
        }


class EventEdit(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ('event_name', 'event_start', 'event_end', 'comment')
        widgets = {
            'event_name': forms.TextInput(),
            'event_start': forms.DateInput(),
            'event_end': forms.DateInput(),
        }


class MemberCreate(forms.ModelForm):
    membership_fee = forms.DecimalField(label=_('Cuota de membresía'))

    class Meta:
        model = models.Member
        fields = 'person',
        widgets = {
            'person': forms.HiddenInput(),
        }

    def save(self, *args, **kwargs):
        membership_data = {
            'membership_fee': self.cleaned_data['membership_fee']
        }
        self.instance.membership = models.Membership(**membership_data)
        return super().save(*args, **kwargs)


class MemberEdit(forms.ModelForm):

    class Meta:
        model = models.Member
        fields = (
            'category',
            'id_card_status',
            'ss_card_status',
            'dpa_status',
            'photo_status',
            'card_status',
            'bursary',
            'photo')


class MembershipCreate(forms.ModelForm):
    class Meta:
        model = models.Membership
        fields = 'payment_status',

        widgets = {
            'payment_status': forms.HiddenInput(),
        }


class MembershipEdit(forms.ModelForm):

    class Meta:
        model = models.Membership
        fields = ('type_of_membership', 'payment_status', 'membership_fee', 'membership_status')


class CustodianEdit(forms.ModelForm):
    class Meta:
        model = models.Custodian
        fields = 'category', 'authorized_signature', 'emergency_contact',
        widgets = {
            'authorized_signature': forms.TextInput(),
            'emergency_contact': forms.TextInput(),
        }


class GroupCreate(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('group_name', 'project')
        widgets = {
            'group_name': forms.TextInput(),
            'project': forms.Select()
        }


class GroupEdit(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('group_name',)


class ProjectCreate(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ('project_name', 'date_start', 'date_end', 'comment')
        widgets = {
            'project_name': forms.TextInput(),
            'date_start': forms.DateInput(),
            'date_end': forms.DateInput(),
            'comment': forms.TextInput(),
        }


class ProjectEdit(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ('project_name', 'date_start', 'date_end', 'comment',)
        widgets = {
            'project_name': forms.TextInput(),
            'date_start': forms.DateInput(),
            'date_end': forms.DateInput(),
        }


class NewIndividualMember(forms.Form):
    name = forms.CharField(label=_('Nombre'))
    surname = forms.CharField(label=_('Apellidos'))
    phone = forms.CharField(label=_('Teléfono'))
    adress = forms.CharField(label=_('Dirección'))
    mail = forms.EmailField(label=_('Correo electrónico'))
    id_number = forms.CharField(label='DNI')

    membership_fee = D('15.00')

    def execute(self):
        cleaned_data = self.cleaned_data
        membership = models.Membership.objects.create(membership_fee=self.membership_fee)
        person = models.Person.objects.create(
            name=cleaned_data['name'],
            surname=cleaned_data['surname'],
            phone_number=cleaned_data['phone'],
            address_street=cleaned_data['adress'],
            id_number=cleaned_data['id_number'],
            email=cleaned_data['mail'])
        models.Member.objects.create(person=person, membership=membership)

        return membership


class NewFamilyMember(forms.Form):

    name1 = forms.CharField(label=_('Nombre'))
    phone1 = forms.CharField(label=_('Teléfono'))
    surname1 = forms.CharField(label=_('Apellidos'))
    id_number1 = forms.CharField(label='DNI')
    mail1 = forms.CharField(label=_('Correo electrónico'))

    name2 = forms.CharField(label=_('Nombre'))
    phone2 = forms.CharField(label=_('Teléfono'))
    surname2 = forms.CharField(label=_('Apellidos'))
    id_number2 = forms.CharField(label='DNI')
    mail2 = forms.CharField(label=_('Correo electrónico'))

    name3 = forms.CharField(label=_('Nombre'))
    phone3 = forms.CharField(label=_('Teléfono'))
    surname3 = forms.CharField(label=_('Apellidos'))
    id_number3 = forms.CharField(label='DNI')
    mail3 = forms.CharField(label=_('Correo electrónico'))

    name4 = forms.CharField(label=_('Nombre'))
    phone4 = forms.CharField(label=_('Teléfono'))
    surname4 = forms.CharField(label=_('Apellidos'))
    id_number4 = forms.CharField(label='DNI')
    mail4 = forms.CharField(label=_('Correo electrónico'))

    membership_fee = D('40.00')

    def execute(self):
        cleaned_data = self.cleaned_data
        membership = models.Membership.objects.create(membership_fee=self.membership_fee)
        for i in range(1, 5):
            person = models.Person.objects.create(
                name=cleaned_data['name' + str(i)],
                surname=cleaned_data['surname' + str(i)],
                phone_number=cleaned_data['phone' + str(i)],
                id_number=cleaned_data['id_number' + str(i)],
                email=cleaned_data['mail' + str(i)],
            )
            models.Member.objects.create(person=person, membership=membership)

        return membership


class CreateCustodian(forms.ModelForm):
    class Meta:
        model = models.Custodian
        fields = 'category', 'minor', 'person'
        widgets = {
            'minor': forms.HiddenInput(),
        }


class CreateCustodianFromPerson(forms.Form):
    category = forms.ChoiceField(label=_('Tipo'), choices=models.Custodian.CATEGORIES, required=False)
    person = forms.UUIDField(label=_('Selecciona persona'), required=False)

    def clean_person(self):
        person_uuid = self.cleaned_data['person']
        if not person_uuid:
            return
        try:
            person = models.Person.objects.get(pk=person_uuid)
        except models.Person.DoesNotExist:
            return
        return person

    def __init__(self, minor, *args, **kwargs):
        self.minor = minor
        super().__init__(*args, **kwargs)

    def save(self):
        person = self.cleaned_data['person']
        category = self.cleaned_data['category']
        if not person:
            return

        kwargs = {'person': person, 'minor': self.minor, 'category': category}
        if not models.Custodian.objects.filter(**kwargs).exists():
            return models.Custodian.objects.create(**kwargs)
