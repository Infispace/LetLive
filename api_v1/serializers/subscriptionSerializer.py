from rest_framework import serializers
from home.models import AppUser
from home.models import Author
from home.models import Subscriber
from home.models import change_user_groups


class SubscriptionSerializer(serializers.Serializer):
    groups = serializers.MultipleChoiceField(choices=AppUser.USER_LEVEL)

    def save(self):
        request = self.context['request']
        groups = self.validated_data['groups']
        
        change_user_groups(
            request.user,
            groups
        )

