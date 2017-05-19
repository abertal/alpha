from modeltranslation.translator import translator, TranslationOptions

from .models import Person


class PersonTranslationOptions(TranslationOptions):
    fields = ('name', 'surname')


translator.register(Person, PersonTranslationOptions)
