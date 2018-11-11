from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView, Response
from rest_framework import generics, pagination, status

from orders.models import DefaultOrder, OrderItem
from orders.serializers import OrderSerializer
from orders.tasks import UserOrderNotification, AdminOrderNotification
from cart.cart import Cart


class OrderAPIView(APIView):

    model = DefaultOrder
    serializer = OrderSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        return Response({})


class OrdesrPagination(pagination.PageNumberPagination):
    page_size = 100


class OrdersListAPIView(generics.ListAPIView):

    model = DefaultOrder
    serializer_class = OrderSerializer
    pagination_class = OrdesrPagination

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at', 'id')

    def post(self, request, *args, **kwargs):
        cart = Cart(request.session)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for item in cart.items:
                instance = OrderItem(
                    order=order,
                    product=item.product,
                    price=item.price,
                    quantity=item.quantity
                )
                instance.save()
            cart.clear()
            UserOrderNotification.apply_async((order.pk,), countdown=10)
            AdminOrderNotification.apply_async((order.pk,), countdown=10)
            return Response(
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    def put(self, request, *args, **kwargs):
        return Response({})
