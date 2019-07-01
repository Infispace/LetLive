from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.HyperlinkedIdentityField(
        many=True,
        view_name='api_v1:group-detail',
    )

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'groups')
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:user-detail',
                'lookup_field': 'pk'
            },
        }
