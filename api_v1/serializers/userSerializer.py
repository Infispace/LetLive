from django.contrib.auth.models import User
from rest_framework import serializers
from home.models import Subscriber
from home.models import Author
from home.models import Publisher
from home.models import Admin
from home.models import AppUser


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

class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        #read_only=True,
        view_name='api_v1:user-detail',
        queryset=User.objects.filter(is_active=True),
    )
    
    #subscription_type = serializers.

    class Meta:
        model = Subscriber
        fields = (
            'url', 
            'id', 
            'user', 
            'telephone', 
            'address', 
            'user_level',
            'subscription_type'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:subscriber-detail',
                'lookup_field': 'pk'
            },
        }


