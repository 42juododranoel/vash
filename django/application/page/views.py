from django.views.generic.detail import DetailView

from page.models import Page
from page.rest import PageSerializer


class BasePageDetailView(DetailView):
    model = Page
    template_name = 'page/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serialized_page = PageSerializer(self.object)
        context['object'] = context['page'] = serialized_page.data
        return context

    def get_template_names(self):
        return [self.object.template.file.file.name]


class VisiblePageDetailView(BasePageDetailView):
    queryset = Page.objects.visible()


class InvisiblePageDetailView(BasePageDetailView):
    queryset = Page.objects.invisible()
