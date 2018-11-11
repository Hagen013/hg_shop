##############################################################################
#                                  Displayable                               #
##############################################################################
from django.db import models

class DisplayableManager(models.Manager):

    def get_queryset(self):
        return super(DisplayableManager, self).get_queryset().\
            filter(is_published=True)


class Displayable(models.Model):
    """
    Displayable - всё то, что может быть отображено на странице.
    created_at  |
    modified_at | - даты
    scoring - рейтинг, ранжирование
    is_published - опубликована, связзано с DisplayableManager
    """
    class Meta:
        abstract = True

    # Custom menager
    objects = models.Manager()
    public = DisplayableManager()

    scoring = models.IntegerField(
        verbose_name='Скоринг',
        default=1000000,
    )

    # Date Fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее изменение'
    )
    # Boolean Fields
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликован'
    )

    def save(self, *args, **kwargs):
        super(Displayable, self).save(*args, **kwargs)