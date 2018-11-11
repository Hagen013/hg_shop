from rest_framework import serializers

from core.serializers import DynamicFieldsModelSerializer
from .models import DefaultOrder

class OrderSerializer(DynamicFieldsModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DefaultOrder
        fields = (
            'id',
            'status',
            'order_text',
            'notified',
            'name',
            'phone',
            'email',
            'address',
            'created_at',
            'modified_at',
            'total_price'
        )
