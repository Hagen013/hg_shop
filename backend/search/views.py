from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector

from digg_paginator import DiggPaginator

from core.models import ProductPage


class SearchPageView(ListView):
    """
    Класса обработки запросов search-form из базового шаблона
    """
    template_name = "pages/search_page.html"
    context_object_name = 'items_list'
    paginator_class = DiggPaginator
    paginate_by = 40

    def __init__(self, *args, **kwargs):
        super(SearchPageView, self).__init__(*args, **kwargs)
        self.query = None

    def get(self, request, *args, **kwargs):
        self.query = str(request.GET['q'])
        return (super(SearchPageView, self).get(request, *args, **kwargs))

    def get_queryset(self):
        qs = ProductPage.objects.annotate(
            search=SearchVector('_fts_body'),).filter(search=self.query)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(SearchPageView, self).get_context_data(**kwargs)
        context['search_query'] = self.query
        return context


