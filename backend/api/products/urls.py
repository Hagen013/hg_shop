from django.conf.urls import url, include

from .views import ProductPageAPIView, ProductPageListAPIView

urlpatterns = ([
    url(r'^$', ProductPageListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>(([\d]+)))/$', ProductPageAPIView.as_view(), name='details'),
])