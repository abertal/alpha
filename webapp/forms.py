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
        person = Person.objects.create(name=cleaned_data['name'],
        surname=cleaned_data['surname'], 
        phone_number=cleaned_data['phone'],
        address_street=cleaned_data['adress'],
        id_number=cleaned_data['id_number'],
        email=cleaned_data['mail'])
        print(person)


class NewFamilyMember(forms.Form):
    name1 = forms.CharField()
    phone1 = forms.CharField()
    name2 = forms.CharField()
    phone2 = forms.CharField()

    def execute(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        person1 = Person.objects.create(name=cleaned_data['name1'])
        person2 = Person.objects.create(name=cleaned_data['name2'])
        print(person1)
        print(person2)
