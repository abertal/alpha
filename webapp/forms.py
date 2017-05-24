from decimal import Decimal as D

from django import forms
from django.utils.translation import ugettext_lazy as _

from core import models


class CreatePerson(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ('name', 'surname',)

        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
        }


class EditPerson(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = (
            'name', 'surname', 'birthday',
            'id_number', 'ss_number',
            'phone_number', 'mobile_number', 'email',
            'address_street', 'address_locality', 'postal_code', 'address_region', 'address_country',
            'health_warnings', 'comment',
        )
        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
            'id_number': forms.TextInput(),
            'ss_number': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'mobile_number': forms.TextInput(),
            'address_locality': forms.TextInput(),
            'postal_code': forms.TextInput(),
            'address_region': forms.TextInput(),
            'address_country': forms.TextInput(),
        }


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
        fields = 'category', 'courses', 'sibling',


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
