from django.contrib.auth.models import User
from rest_framework import serializers
from home.models import Subscriber
from home.models import AppUser


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
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:subscriber-detail',
                'lookup_field': 'pk'
            },
        }

    #def create(self, validated_data):
        #Subscriber.objects.create_user(
        #    username=self.form.cleaned_data['username'],
        #    email=self.form.cleaned_data['email'],
        #    password=password,
        #    user_level= user_level
        #)

