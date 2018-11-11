from django.conf.urls import url, include

from .views import CategoryPageListAPIView

urlpatterns = ([
    url(r'^$', CategoryPageListAPIView.as_view(), name='list'),
])