from django.conf.urls import url, include

from .views import LoginView, AdminAppView


urlpatterns = [
    url(r'^$', AdminAppView.as_view(), name='main'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
