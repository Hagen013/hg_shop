from django.conf.urls import url, include

from .views import OrderView, OrderSuccessView, OrderCancelledView


app_name = 'orders'

urlpatterns = [
    url(r'^$', OrderView.as_view(), name='View'),
    url(r'^success/$', OrderSuccessView.as_view(), name='success'),
    url(r'^cancelled/$', OrderCancelledView.as_view(), name='cancelled'),
]
