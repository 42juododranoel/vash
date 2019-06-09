"""
This stuff was a mistake,
but it has helped me to learn the right way.
Hope I will rewrite it some day.
"""
from django import forms
from django_ace import AceWidget
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from template.models import Template


class TemplateForm(forms.ModelForm):
    content = forms.CharField(
        widget=AceWidget(**settings.ACE_WIDGET_OPTIONS),
        required=False,
    )

    class Meta:
        model = Template
        fields = ['name', 'content', 'file']
        help_texts = {'file': _('Gets overwritten on save with content specified above')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            with open(self.instance.file.path, 'r') as file:
                self.fields['content'].initial = file.read()
        except Template.file.RelatedObjectDoesNotExist:
            pass  # During creating new template

    def save(self, commit=True):
        self.instance = super().save(commit=commit)
        with open(self.instance.file.path, 'w') as file:
            file.write(self.cleaned_data['content'])
        return self.instance


@admin.register(Template)
class TemplateModelAdmin(admin.ModelAdmin):
    form = TemplateForm
