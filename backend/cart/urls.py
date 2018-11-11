from django.conf.urls import url, include

from .views import CartDetailView, Remove, Add, Update, CartInfo


urlpatterns = [
    url(r'^$', CartDetailView.as_view(), name='default'),
    url(r'^remove/(?P<product_id>\d+)/$', Remove, name='delete'),
    url(r'^add/$', Add, name='add'),
    url(r'^update/$', Update, name='update'),
    url(r'^info/$', CartInfo, name='info'),
]
