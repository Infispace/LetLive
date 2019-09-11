from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for the django User model
    '''
    groups = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='api_v1:group-detail',
    )
    
    class Meta:
        model = User
        exclude = ['password', 'user_permissions']
        
        read_only_fields = [
            "is_superuser",
            "is_staff",
            "is_active",
            'last_login',
            'date_joined',
        ]

        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:user-detail',
                'lookup_field': 'pk'
            },
        }

