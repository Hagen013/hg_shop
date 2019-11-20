from django.conf.urls import url, include

from .views import (ProductPageAPIView,
                    ProductPageListAPIView,
                    ProductImagesAPIView,
                    ProductImageUploadView,
                    ProductImagesUploadView)

urlpatterns = ([
    url(r'^$', ProductPageListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>(([\d]+)))/$', ProductPageAPIView.as_view(), name='details'),
    url(r'^(?P<pk>(([\d]+)))/images/$', ProductImagesAPIView.as_view(), name='images'),
    url(r'^(?P<pk>(([\d]+)))/image/$', ProductImageUploadView.as_view(), name='main_image'),
    url(r'^(?P<pk>(([\d]+)))/images/upload/$', ProductImagesUploadView.as_view(), name='images-upload'),
])