##############################################################################
#                                  BaseProduct                               #
##############################################################################

from django.db import models
from django.forms.models import model_to_dict
from django.contrib.postgres.fields import JSONField

from .category_page import CategoryPage
from .fields import NameField, DescriptionField


class BaseProduct(models.Model):
    """
    Базовый абстрактный класс продукта
    name - наименования товара
    description - описание товара
    model - модель товара
    price - цена
    vendor_code - артикул
    old_price - старая цена
    is_in_stock - в продаже
    is_new_product - новый продукт
    is_bestseller - бесцеллер
    as_product - Вывод всех полей продукта
    """
    class Meta:
        abstract = True
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = NameField()
    description = DescriptionField()

    price = models.FloatField(
        verbose_name='Цена'
    )

    base_price = models.FloatField(
        default=0,
        verbose_name='Базовая цена'
    )

    old_price = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Старая цена'
    )

    # Внешний ключ на категорию
    category = models.ForeignKey(
        CategoryPage,
        verbose_name="категория",
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
    )

    _amount = models.PositiveIntegerField(
        verbose_name='количество',
        default=1
    )

    vendor_code = models.PositiveIntegerField(
        verbose_name='Артикул',
        unique=True,
        db_index=True,
    )

    attributes = JSONField(
        verbose_name='аттрибуты',
        blank=True
    )

    # Boolean fields
    is_in_stock = models.BooleanField(
        default=True,
        verbose_name='В наличии'
    )
    is_new_product = models.BooleanField(
        default=False,
        verbose_name='Новинка',
        db_index=True,
    )
    is_bestseller = models.BooleanField(
        default=False,
        verbose_name='Бестселлер',
        db_index=True,
    )


    def as_product(self):
        return model_to_dict(self, fields=[field.name
                                           for field in BaseProduct._meta.fields])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(BaseProduct, self).save(*args, **kwargs)
