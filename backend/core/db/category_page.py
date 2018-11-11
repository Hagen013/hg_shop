##############################################################################
#                                  CategoryPage                              #
##############################################################################
from django.db import models

from mptt.managers import TreeManager

from .base_page import BasePage
from .displayable import Displayable
from .base_node import BaseNode
from .image import Image


class CategoryPage(BaseNode, BasePage, Displayable, Image):
    """
    Страница категории - станица иерархического (mptt) каталога
    """
    class Meta():
        abstract = False
        verbose_name = 'category page'
        verbose_name_plural = 'category pages'

    page_type = "category_page"
    objects = TreeManager()
    upload_image_to = 'images'

    default_scoring = models.IntegerField(
        default=10000,
        verbose_name='рейтинг товаров в категории',
    )

    def get_full_url(self):
        path = self.get_ancestors(include_self=True)
        url = '/'.join(list(map(lambda item: str(item.slug), path)))
        return url

    def get_absolute_url(self):
        return '/catalog/' + self.url

    def __repr__(self):
        return '<CategoryPage: {0}>'.format(self.name)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            ancestors = self.parent.get_ancestors(include_self=True)
            path = list(map(lambda x: x.slug, ancestors))
            path.append(self.slug)
            path = '/'.join(path)
            self.url = path
        super(CategoryPage, self).save(*args, **kwargs)

    def move_to(self, *args, **kwargs):
        super(CategoryPage, self).move_to(*args, **kwargs)
        self.save()
