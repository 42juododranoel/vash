from django import forms
from django_ace import AceWidget
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from snippet.models import Snippet


class SnippetForm(forms.ModelForm):
    class Meta:
        editor_widget = AceWidget(**settings.ACE_WIDGET_OPTIONS)
        widgets = {'content': editor_widget}
        fields = ['content']
        model = Snippet


@admin.register(Snippet)
class SnippetModelAdmin(admin.ModelAdmin):
    form = SnippetForm
    save_on_top = True
    list_display = ['name', 'slug']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ['name', 'slug']}),
        (_('Dates'), {'fields': ['created_at', 'updated_at']}),
        (_('Content'), {'fields': ['content']}),
    )


class SnippetInline(admin.StackedInline):
    model = Snippet
    form = SnippetForm
    extra = 0
    fields = ['name', 'slug', 'content']
