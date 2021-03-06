from django.conf.urls import url, include

from .views import LoginView, AdminAppView


app_name = 'md-admin'


urlpatterns = [
    url(r'^$', AdminAppView.as_view(), name='main'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
