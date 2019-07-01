from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')
        
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:group-detail',
                'lookup_field': 'pk'
            },
        }
