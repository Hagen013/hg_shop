from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap, index
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.sites.models import Site, SiteManager
from django.urls import reverse

from core.models import ProductPage, CategoryPage


class StaticViewSitemap(Sitemap):

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='torgosvet.ru', name='torgosvet.ru')
        return super(StaticViewSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return [
            'core:index_page',
            'core:about',
            'core:optom',
            'core:contacts',
            'core:info',
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static_pages': StaticViewSitemap,

    'categories': GenericSitemap({
        'queryset': CategoryPage.objects.all(),
        'date_field': 'modified_at',
    }),

    'products': GenericSitemap({
        'queryset': ProductPage.objects.all(),
        'date_field': 'modified_at',
    }),
}

urlpatterns = [
    url(r'\.xml/$', index, {'sitemaps': sitemaps}),
    url(r'-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]