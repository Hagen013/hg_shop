from django.conf.urls import url

from .views import AdminSessionLoginAPIView, SessionUserAPIView


urlpatterns = ([
    url(r'^session/$', SessionUserAPIView.as_view()),
    url(r'^admin/login/$', AdminSessionLoginAPIView.as_view())
])
