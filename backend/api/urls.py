from django.conf.urls import url, include

from .cart import urls as cart_urls
from .orders import urls as orders_urls
from .users import urls as users_urls
from .products import urls as products_urls
from .categories import urls as categories_urls


urlpatterns = [
    url(r'^cart/', include(cart_urls)),
    url(r'^orders/', include(orders_urls)),
    url(r'^users/', include(users_urls)),
    url(r'^products/', include(products_urls)),
    url(r'^categories/', include(categories_urls))
]
