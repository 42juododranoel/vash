from django.urls import path

from page.views import (
    VisiblePageDetailView,
    InvisiblePageDetailView,
)

app_name = 'page'
urlpatterns = [
    path(
        '<slug:slug>',
        VisiblePageDetailView.as_view(),
        name='visible'
    ),
    path(
        'preview/<slug:slug>',
        InvisiblePageDetailView.as_view(),
        name='invisible'
    ),
    path(
        '',
        VisiblePageDetailView.as_view(),
        kwargs={'slug': 'main'},
        name='main'
    ),
]
