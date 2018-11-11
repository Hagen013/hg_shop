from rest_framework import serializers

from core.serializers import ProductPageSerializer


class CartItemSerializer(serializers.Serializer):

    product = ProductPageSerializer()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()

class CartSerializer(serializers.Serializer):

    items = CartItemSerializer(many=True)
    is_empty = serializers.BooleanField()
    count = serializers.IntegerField()
    total_price = serializers.IntegerField()
