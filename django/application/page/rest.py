from rest_framework import serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from page.models import Page


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ('title', 'link', 'cache_link', 'clean_meta', 'clean_content')


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.visible()
    serializer_class = PageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'slug': ['in']}
