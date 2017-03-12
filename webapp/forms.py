from decimal import Decimal as D

from django import forms

from core import models


class EditPerson(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = 'name', 'surname'


class NewIndividualMember(forms.Form):
    name = forms.CharField(label='Nombre')
    surname = forms.CharField(label='Apellidos')
    phone = forms.CharField(label='Teléfono')
    adress = forms.CharField(label='Dirección')
    mail = forms.EmailField(label='Correo electrónico')
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
        models.PersonMembership.objects.create(person=person, membership=membership)

        return membership


class NewFamilyMember(forms.Form):

    name1 = forms.CharField(label='Nombre')
    phone1 = forms.CharField(label='Teléfono')
    surname1 = forms.CharField(label='Apellidos')
    id_number1 = forms.CharField(label='DNI')
    mail1 = forms.CharField(label='Correo electrónico')

    name2 = forms.CharField(label='Nombre')
    phone2 = forms.CharField(label='Teléfono')
    surname2 = forms.CharField(label='Apellidos')
    id_number2 = forms.CharField(label='DNI')
    mail2 = forms.CharField(label='Correo electrónico')

    name3 = forms.CharField(label='Nombre')
    phone3 = forms.CharField(label='Teléfono')
    surname3 = forms.CharField(label='Apellidos')
    id_number3 = forms.CharField(label='DNI')
    mail3 = forms.CharField(label='Correo electrónico')

    name4 = forms.CharField(label='Nombre')
    phone4 = forms.CharField(label='Teléfono')
    surname4 = forms.CharField(label='Apellidos')
    id_number4 = forms.CharField(label='DNI')
    mail4 = forms.CharField(label='Correo electrónico')

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
            models.PersonMembership.objects.create(person=person, membership=membership)

        return membership
