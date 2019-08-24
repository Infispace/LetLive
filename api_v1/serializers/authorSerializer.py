from .dynamicFieldsHModelSerializer import DynamicFieldsHModelSerializer
from rest_framework.serializers import HyperlinkedRelatedField
from django.contrib.auth.models import User
from home.models import Author
from home.models import AppUser


class AuthorSerializer(DynamicFieldsHModelSerializer):
    user = HyperlinkedRelatedField(
        many=False,
        view_name='api_v1:user-detail',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:author-detail',
                'lookup_field': 'pk'
            },
        }

