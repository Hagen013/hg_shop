from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView, Response
from rest_framework import status

from core.models import CategoryPage
from core.serializers import CategoryPageSerializer


class CategoryPageListAPIView(APIView):

    model = CategoryPage
    serializer = CategoryPageSerializer

    def get(self, request, *args, **kwargs):
        qs = CategoryPage.objects.all()
        serialzier = self.serializer(qs, many=True)
        return Response(
            serialzier.data,
            status=status.HTTP_200_OK
        )
