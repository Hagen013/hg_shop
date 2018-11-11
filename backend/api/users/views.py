from django.contrib.auth import authenticate, login

from rest_framework.views import APIView, Response
from rest_framework import status

from .serializers import SessionUserSerializer


class AdminSessionLoginAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if (username is None) or (password is None):
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                login(request, user)
                if user.is_superuser:
                    return Response(
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        status=status.HTTP_403_FORBIDDEN
                    )


class SessionUserAPIView(APIView):

    serializer = SessionUserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        serializer = self.serializer(user)
        print(serializer.data)
        print(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )