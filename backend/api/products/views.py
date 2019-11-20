from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import transaction

from rest_framework.views import APIView, Response
from rest_framework import generics, pagination, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser

from core.models import ProductPage, ProductPhoto
from core.serializers import (ProductPageSerializer,
                              ProductPhotoSerializer,
                              ProductImageFileSerializer)

from api.views import ListViewMixin


class ProductPageListAPIView(APIView, ListViewMixin):

    model = ProductPage
    serializer_class = ProductPageSerializer
    pagination_class = LimitOffsetPagination
    permissions_class = permissions.IsAdminUser

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def filter_queryset(self, qs):
        qs = super(ProductPageListAPIView, self).filter_queryset(qs)
        vendor_code = self.request.GET.get('vendor_code', None)
        if vendor_code is not None:
            qs = qs.filter(vendor_code__startswith=vendor_code)
        return qs


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
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImagesAPIView(APIView):

    model            = ProductPhoto
    serializer_class = ProductPhotoSerializer
    permissions_class = permissions.IsAdminUser

    def get(self, request, pk):
        images = self.model.objects.filter(
            product=pk
        )
        serializer = self.serializer_class(images, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        stored_images = self.model.objects.filter(
            product=pk
        )
        
        received_images = request.data
        received_images_mapping = {}
        for image in received_images:
            received_images_mapping[image['id']] = {
                'order': image['order']
            }

        with transaction.atomic():
            for image in stored_images:
                received = received_images_mapping.get(image.id, None)
                if received is None:
                    image.delete()
                else:
                    if image.order != received['order']:
                        image.order = received['order']
                        image.save()
        
        return Response({})


class ProductImageUploadView(APIView):

    model = ProductPage
    permissions_class = permissions.IsAdminUser
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)

    def get_instance(self, pk):
        try:
            return self.model.objects.get(
                pk=pk
            )
        except ObjectDoesNotExist:
            raise Http404


    def put(self, request, pk):
        instance = self.get_instance(pk)
        imageFile = request.FILES.get('image', None)
        if imageFile is not None:
            fs = FileSystemStorage()
            filepath = '{MEDIA_ROOT}images/{model}/{name}'.format(
                MEDIA_ROOT=settings.MEDIA_ROOT,
                model=instance.vendor_code,
                name=imageFile.name
            )
            filename = fs.save(filepath, imageFile).replace(settings.MEDIA_ROOT, '')
            instance.image = filename
            instance.save()
            instance.image.close()
            instance.thumbnail.close()
        return Response({})


class ProductImagesUploadView(APIView):

    model = ProductPage
    permissions_class = permissions.IsAdminUser
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)
    serializer_class = ProductImageFileSerializer

    def get_instance(self, pk):
        try:
            return self.model.objects.get(
                pk=pk
            )
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, pk):
        instance = self.get_instance(pk)
        count = instance.productphoto_set.all().count()
        files = request.FILES.keys()
        fs = FileSystemStorage()
        for key in files:
            count += 1
            image_file = request.FILES[key]
            serializer = self.serializer_class(instance, image_file, fs, count)
            serializer.save()
        data = ProductPhotoSerializer(instance.productphoto_set.all(), many=True).data
        return Response(
            data,
            status=status.HTTP_200_OK
        )