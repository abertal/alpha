from django import forms

from mtr.utils.forms import GlobalInitialFormMixin
from mtr.utils.helpers import model_choices

from .lib.manager import manager

from .models import Settings, Field


# TODO: refactor

class SettingsAdminForm(GlobalInitialFormMixin, forms.ModelForm):

    class Meta:
        exclude = tuple()
        model = Settings

    def __init__(self, *args, **kwargs):
        super(SettingsAdminForm, self).__init__(*args, **kwargs)

        self.fields['processor'] = forms.ChoiceField(
            label=self.fields['processor'].label,
            choices=manager.processor_choices(),
            initial=self.fields['processor'].initial,
            help_text=self.fields['processor'].help_text,
            required=self.fields['processor'].required)

        self.fields['dataset'] = forms.ChoiceField(
            label=self.fields['dataset'].label,
            choices=(('', '----'),) + tuple(manager.dataset_choices()),
            initial=self.fields['dataset'].initial,
            help_text=self.fields['dataset'].help_text,
            required=self.fields['dataset'].required)

        self.fields['data_action'] = forms.ChoiceField(
            label=self.fields['data_action'].label,
            choices=(('', '----'),) + tuple(manager.action_choices()),
            initial=self.fields['data_action'].initial,
            help_text=self.fields['data_action'].help_text,
            required=self.fields['data_action'].required)

        self.fields['model'] = forms.ChoiceField(
            label=self.fields['model'].label,
            choices=model_choices(),
            required=self.fields['model'])


class FieldInlineAdminForm(forms.ModelForm):

    class Meta:
        exclude = tuple()
        model = Field

    def __init__(self, *args, **kwargs):
        super(FieldInlineAdminForm, self).__init__(*args, **kwargs)

        self.fields['converters'] = forms.ChoiceField(
            label=self.fields['converters'].label,
            required=self.fields['converters'].required,
            choices=manager.converter_choices())
