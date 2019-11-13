from django.conf.urls import url
from .views import SearchPageView

app_name = 'search'

urlpatterns = [
    url(r'^', SearchPageView.as_view(), name="search_page"),
]
