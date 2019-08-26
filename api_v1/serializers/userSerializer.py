from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for the django User model
    '''
    groups = serializers.HyperlinkedIdentityField(
        many=True,
        view_name='api_v1:group-detail',
    )
    
    read_only_fields = ['username']

    class Meta:
        model = User
        exclude = ['password','user_permissions']
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:user-detail',
                'lookup_field': 'pk'
            },
        }

