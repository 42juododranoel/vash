import filer.urls
import rest_framework.urls
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from django.conf.urls.static import static

import page.urls
from page.rest import PageViewSet


router = routers.DefaultRouter()
router.register(r'page', PageViewSet, base_name='page')

urlpatterns = [
    path('api/auth/', include(rest_framework.urls, 'rest_framework')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('file/', include(filer.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

urlpatterns += [path('', include(page.urls, 'page'))]
