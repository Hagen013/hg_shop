from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework import status

from cart.cart import Cart
from cart.serializers import CartSerializer
from core.models import ProductPage
from core.serializers import ProductPageSerializer


class CartAPIView(APIView):

    def post(self, request, *args, **kwargs):
        cart = Cart(request.session)
        pk = request.POST.get('pk')
        quantity = request.POST.get('quantity')
        instance = ProductPage.objects.get(id=pk)
        try:
            instance = ProductPage.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        cart.add(
            product=instance,
            price=instance.price,
            quantity=quantity,
        )
        return Response(
            status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        cart = Cart(request.session)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        cart = Cart(request.session)
        pk = request.data.get('pk')
        quantity = int(request.data.get('quantity'))
        try:
            instance = ProductPage.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        cart.set_quantity(instance, quantity)
        return Response(
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        cart = Cart(request.session)
        pk = request.query_params.get('pk')
        try:
            instance = ProductPage.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        cart.remove(instance)
        return Response(
            status=status.HTTP_200_OK
        )
