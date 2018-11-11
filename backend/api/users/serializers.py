from rest_framework import serializers


class SessionUserSerializer(serializers.Serializer):

    is_authenticated = serializers.BooleanField()
    is_staff = serializers.BooleanField()

    class Meta:
        fields = (
            'is_authenticated',
            'is_staff'
        )
