from django import forms
from django_ace import AceWidget
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from page.models import Page


class PageForm(forms.ModelForm):
    class Meta:
        editor_widget = AceWidget(
            mode='html',
            theme='xcode',
            width='100%',
            wordwrap=True,
            tabsize=2,
        )
        widgets = {'content': editor_widget}
        fields = ['content']
        model = Page


@admin.register(Page)
class PageModelAdmin(admin.ModelAdmin):
    form = PageForm
    ordering = ['-is_published', '-id']
    save_on_top = True
    list_display = ['title', 'is_published', 'slug']
    readonly_fields = ['updated_at']
    fieldsets = (
        (None, {
            'fields': [
                'title',
                'slug',
                'template',
                'is_published',
                'keywords',
                'description',
                'open_graph_image',
            ],
        }),
        (_('Dates'), {'fields': ['created_at', 'updated_at']}),
        (_('SEO'), {'fields': ['seo_keywords', 'seo_description']}),
        (_('Content'), {'fields': ['content']}),
    )
