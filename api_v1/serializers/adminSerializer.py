from .dynamicFieldsHModelSerializer import DynamicFieldsHModelSerializer
from rest_framework.serializers import HyperlinkedRelatedField
from django.contrib.auth.models import User
from home.models import Admin
from home.models import AppUser


class AdminSerializer(DynamicFieldsHModelSerializer):
    user = HyperlinkedRelatedField(
        many=False,
        view_name='api_v1:user-detail',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:admin-detail',
                'lookup_field': 'pk'
            },
        }

