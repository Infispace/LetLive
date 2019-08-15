from django.contrib.auth.models import User
from rest_framework import serializers
from home.models import Admin
from home.models import AppUser


class AdminSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        #read_only=True,
        view_name='api_v1:user-detail',
        queryset=User.objects.filter(is_active=True),
    )

    class Meta:
        model = Admin
        fields = (
            'url', 
            'id', 
            'user', 
            'telephone', 
            'address', 
            'user_level',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:admin-detail',
                'lookup_field': 'pk'
            },
        }

