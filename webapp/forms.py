from django import forms

from core.models import Person


class NewIndividualMember(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()

    def execute(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        person = Person.objects.create(name=cleaned_data['name'])
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
