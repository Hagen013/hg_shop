##############################################################################
#                                  BasePage                                  #
##############################################################################
from django.db import models
from django.forms.models import model_to_dict

from .fields import NameField, DisplayableSlugField, DisplayableURLField


class BasePage(models.Model):
    """
    Абстрактный класс BasePage (Базовая страница).
    Неразрывно связан c классом Displayable. Displayable вынесен из
    BasePage ради DRY, в случаях когда существуют сущности Displayable,
    но не имеющие собственной страницы, напримет группа товаров связанная
    с одной страницей (DisplayableProduct)
    page_type - тип страницы(каталог, категория, карточка товара),
    должно быть переопределено в потомках
    meta_title - мета заголовок
    meta_keywords - ключевые слова
    meta_description - метаописание
    get_meta_title)() - метод формирования meta_title
    get_meta_keywords)() - метод формирования meta_keywords
    get_meta_description)() - метод формирования meta_description

    Переопределить если требуется придать особую логику формирования метаполей
    as_page() - выводит все поля класса как страницы
    """
    class Meta:
        abstract = True
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    _meta_title = models.CharField(
        blank=True,
        verbose_name='SEO title',
        max_length=256
    )

    _meta_keywords = models.CharField(
        blank=True,
        verbose_name='SEO keywords',
        max_length=1024
    )

    _meta_description = models.CharField(
        blank=True,
        verbose_name='SEO description',
        max_length=1024
    )

    slug = DisplayableSlugField()
    url = DisplayableURLField()

    def get_full_url(self):
        msg = "Method __get_url() must be implemented by subclass: `{}`"
        raise NotImplementedError(msg.format(self.__class__.__name__))

    #def get_absolute_url(self):
    #    msg = "Method get_absolute_url() must be implemented by subclass: `{}`"
    #    raise NotImplementedError(msg.format(self.__class__.__name__))

    @property
    def page_type(self):
        msg = "page_type must be implemented by subclass: `{}`"
        raise NotImplementedError(msg.format(self.__class__.__name__))

    @property
    def meta_title(self):
        return self.get_meta_title()

    @property
    def meta_keywords(self):
        return self.get_meta_keywords()

    @property
    def meta_description(self):
        return self.get_meta_description()

    def get_meta_title(self):
        return self._meta_title

    def get_meta_keywords(self):
        return self._meta_keywords

    def get_meta_description(self):
        return self._meta_description

    def save(self, *args, **kwargs):
        super(BasePage, self).save(*args, **kwargs)