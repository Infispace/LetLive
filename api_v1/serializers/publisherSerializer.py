from django.contrib.auth.models import User
from rest_framework import serializers
from home.models import Publisher
from home.models import AppUser


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api_v1:user-detail',
        queryset=User.objects.all(),
    )
    
    class Meta:
        model = Publisher
        fields = '__all__'
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:publisher-detail',
                'lookup_field': 'pk'
            },
        }

