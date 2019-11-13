from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from rest_framework import routers

from .views import IndexPageView, CategoryPageView, ProductPageView, CatalogRootView, ProductPageViewSet

app_name = 'core'

router = routers.DefaultRouter()
router.register(r'products', ProductPageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', IndexPageView.as_view(), name='index_page'),
    url(r'^catalog$', CatalogRootView.as_view(), name='catalog_root'),
    url(r'^catalog/(?P<category_url>.+)$',
        CategoryPageView.as_view(), name='category_page'),
    url(r'^products/(?P<slug>.+)$', ProductPageView.as_view(), name='product_page'),
    url(r'^template/$', TemplateView.as_view(template_name='pages/category-new.html'), name='category-new'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^optom/$', TemplateView.as_view(template_name='pages/optom.html'), name='optom'),
    url(r'^contacts/$', TemplateView.as_view(template_name='pages/contacts.html'), name='contacts'),
    url(r'^info/$', TemplateView.as_view(template_name='pages/info.html'), name='info'),
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


