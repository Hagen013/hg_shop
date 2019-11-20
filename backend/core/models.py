from django.db import models
from django.urls import reverse

from .db.product_page import ProductPage
from .db.category_page import CategoryPage
from .db.image import Image


class ProductPhoto(Image):

    upload_image_to = 'images'

    product = models.ForeignKey(
        ProductPage,
        verbose_name="товар",
        on_delete=models.CASCADE,
        db_index=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True
    )
