from django.conf.urls import url

from .views import OrderAPIView, OrdersListAPIView


urlpatterns = ([
    url(r'^$', OrdersListAPIView.as_view()),
    url(r'^(?P<pk>(([\d]+)))/$', OrderAPIView.as_view())
])
