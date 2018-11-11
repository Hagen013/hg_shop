##############################################################################
#                                  BaseCatalog                               #
##############################################################################
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from .fields import NameField, DescriptionField


# Кастомный менеджер для вывода mptt-древовидного qs
class DisplayableNodesManager(TreeManager):

    use_for_related_fields = False

    def get_queryset(self):
        return super(DisplayableNodesManager, self).get_queryset().\
            filter(is_published=True)


class BaseNode(MPTTModel):
    """
    Базовый абстрактный класс каталога,
    Содержит все необходимые поля каталога
    Содержимое каталога пока вытаскивается в представлении
    (Каталог - отдельная сущность.
    Пока тут мало чего но потом может добавиться: картинка, видео,
    какое то поведение)
    """
    class Meta:
        abstract = True

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='потомок',
        db_index=True,
        verbose_name='родительская категория',
        on_delete=models.CASCADE,
    )

    public = DisplayableNodesManager()

    name = NameField()
    description = DescriptionField()
