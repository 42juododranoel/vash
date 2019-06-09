from django import forms
from django_ace import AceWidget
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from page.models import Page
from snippet.admin import SnippetInline


@admin.register(Page)
class PageModelAdmin(admin.ModelAdmin):
    ordering = ['-is_published', '-id']
    save_on_top = True
    list_display = ['title', 'is_published', 'slug', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SnippetInline]
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
                'snippets'
            ],
        }),
        (_('Dates'), {'fields': ['created_at', 'updated_at']}),
        (_('SEO'), {'fields': ['seo_keywords', 'seo_description']}),
    )
