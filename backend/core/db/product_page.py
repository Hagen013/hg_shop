##############################################################################
#                                  ProductPage                               #
##############################################################################
from django.db import models
from django.urls import reverse

from .base_product import BaseProduct
from .base_page import BasePage
from .displayable import Displayable
from .searchable import Searchable
from .image import Image
from .utils import sort_attributes

class ProductPage(BaseProduct, BasePage, Displayable, Searchable, Image):

    class Meta():
        verbose_name = 'product page'
        verbose_name_plural = 'product pages'
        abstract = False

    page_type = "product_page"

    upload_image_to = 'images'

    objects = models.Manager()

    def get_search_body(self):
        return ("{0} {1}".format(self.vendor_code, self.name))

    def get_absolute_url(self):
        return '/products/{0}'.format(self.slug)

    @property
    def has_attributes(self):
        if len(self.attributes) > 0:
            return True
        else:
            return False

    # СЮРПРИЗ: JSONfield выдается в случайном порядке и ORM не сортируется
    # (хранится в алфавитном порядке и при извлечении получает случайный)
    @property
    def sorted_attributes(self):
        if self.has_attributes:
            return sort_attributes(self.attributes)
        else:
            return []

    @property
    def absolute_url(self):
        return reverse('core:product_page', kwargs={'slug': self.slug})
