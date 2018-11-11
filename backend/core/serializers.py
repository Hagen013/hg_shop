from rest_framework import serializers

from .models import ProductPage, CategoryPage


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Serializer модели, принимающий дополнительный аргумент
    'disallowed_fields', который специфицирует неиспользуемые для
    сериализации поля
    """
    def __init__(self, *args, **kwargs):
        # Исключаем из аргументов класса-родителя аргументы полей
        fields = kwargs.pop('fields', None)
        disallowed_fields = kwargs.pop('disallowed_fields', None)

        # Инициализация ModelSerializer
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        _fields = None
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            _fields = existing.difference(allowed)
        elif disallowed_fields is not None:
            disallowed = set(disallowed_fields)
            existing = set(self.fields)
            _fields = existing.intersection(disallowed)

        if _fields is not None:
            for field in _fields:
                self.fields.pop(field)


class ProductPageSerializer(DynamicFieldsModelSerializer):

    image = serializers.ImageField(use_url=True, required=False)
    thumbnail = serializers.ImageField(use_url=True, required=False)
    category_id = serializers.IntegerField()

    class Meta:
        model = ProductPage
        fields = (
            "id",
            "vendor_code",
            "name",
            "description",
            "url",
            "price",
            "old_price",
            "is_in_stock",
            "is_bestseller",
            "is_published",
            "is_new_product",
            "attributes",
            "scoring",
            "image",
            "thumbnail",
            "created_at",
            "modified_at",
            "category_id",
            "_meta_title",
            "_meta_description",
            "_meta_keywords"
        )


class CategoryPageSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = CategoryPage
        fields = (
            "id",
            "parent",
            "name",
            "url"
        )
