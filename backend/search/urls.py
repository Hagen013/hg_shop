from django.conf.urls import url
from .views import SearchPageView


urlpatterns = [
    url(r'^', SearchPageView.as_view(), name="search_page"),
]
