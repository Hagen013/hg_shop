##############################################################################
#                                  Fields Shop                               #
##############################################################################

from django.db import models


class NameField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 500
        kwargs["verbose_name"] = "Наименование"
        super(NameField, self).__init__(*args, **kwargs)


class DescriptionField(models.TextField):

    def __init__(self, *args, **kwargs):
        kwargs["verbose_name"] = "Описание"
        kwargs["blank"] = True
        kwargs['default'] = 'Без описания'
        super(DescriptionField, self).__init__(*args, **kwargs)


class DisplayableSlugField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 1000
        kwargs["unique"] = True
        kwargs["verbose_name"] = "slug"
        super(DisplayableSlugField, self).__init__(*args, **kwargs)


class DisplayableURLField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2000
        kwargs["unique"] = True
        kwargs["verbose_name"] = "URL"
        super(DisplayableURLField, self).__init__(*args, **kwargs)
