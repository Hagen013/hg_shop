from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView, Response
from rest_framework import generics, pagination, status
from rest_framework.exceptions import PermissionDenied

from core.models import ProductPage
from core.serializers import ProductPageSerializer


class ProductPageListAPIView(APIView):

    model = ProductPage
    serializer = ProductPageSerializer

    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        return Response({})


class ProductPageAPIView(APIView):

    model = ProductPage
    serializer = ProductPageSerializer

    def get_instance(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def check_superuser_permissions(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        self.check_superuser_permissions(request)
        instance = self.get_instance(pk)
        print(request.data["category_id"])
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)