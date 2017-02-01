from decimal import Decimal as D

from django import forms

from core import models


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

    name1 = forms.CharField()
    phone1 = forms.CharField()
    surname1 = forms.CharField()
    id_number1 = forms.CharField()
    mail1 = forms.CharField()

    name2 = forms.CharField()
    phone2 = forms.CharField()
    surname2 = forms.CharField()
    id_number2 = forms.CharField()
    mail2 = forms.CharField()

    name3 = forms.CharField()
    phone3 = forms.CharField()
    surname3 = forms.CharField()
    id_number3 = forms.CharField()
    mail3 = forms.CharField()

    name4 = forms.CharField()
    phone4 = forms.CharField()
    surname4 = forms.CharField()
    id_number4 = forms.CharField()
    mail4 = forms.CharField()

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
