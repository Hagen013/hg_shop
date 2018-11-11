from django.db import models

##############################################################################
#                                Searchable                                  #
##############################################################################


class Searchable(models.Model):
    """
    Mixin for Displayable objects
    """
    class Meta():
        abstract = True

    is_searchable = models.BooleanField(
        verbose_name='Отображать в поиске',
        default=True,
    )

    # Костыль для FTS поиска на postgres
    _fts_body = models.CharField(
        'тело поиска',
        max_length=512,
        db_index=True,
        blank=True,
    )

    def get_search_body(self):
        msg = "Method get_absolute_url() must be implemented by subclass: `{}`"
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def save(self, *args, **kwargs):
        self._fts_body = self.get_search_body()
        super(Searchable, self).save(*args, **kwargs)

