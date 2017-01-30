from django import forms

from core.models import Person


class NewIndividualMember(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    phone = forms.CharField()
    adress = forms.CharField()
    mail = forms.CharField()
    id_number = forms.CharField()

    def execute(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        person = Person.objects.create(
            name=cleaned_data['name'],
            surname=cleaned_data['surname'],
            phone_number=cleaned_data['phone'],
            address_street=cleaned_data['adress'],
            id_number=cleaned_data['id_number'],
            email=cleaned_data['mail'])
        return person


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

    def execute(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)

        i = 1

        person1 = Person.objects.create(
            name=cleaned_data['name' + str(i)],
            surname=cleaned_data['surname' + str(i)],
            phone_number=cleaned_data['phone' + str(i)],
            id_number=cleaned_data['id_number' + str(i)],
            email=cleaned_data['mail' + str(i)])
        person2 = Person.objects.create(
            name=cleaned_data['name' + str(i)],
            surname=cleaned_data['surname' + str(i)],
            phone_number=cleaned_data['phone' + str(i)],
            id_number=cleaned_data['id_number' + str(i)],
            email=cleaned_data['mail' + str(i)])
        person3 = Person.objects.create(
            name=cleaned_data['name' + str(i)],
            surname=cleaned_data['surname' + str(i)],
            phone_number=cleaned_data['phone' + str(i)],
            id_number=cleaned_data['id_number' + str(i)],
            email=cleaned_data['mail' + str(i)])
        person4 = Person.objects.create(
            name=cleaned_data['name' + str(i)],
            surname=cleaned_data['surname' + str(i)],
            phone_number=cleaned_data['phone' + str(i)],
            id_number=cleaned_data['id_number' + str(i)],
            email=cleaned_data['mail' + str(i)])

        return person1
