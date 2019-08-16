from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from home.models import Subscriber
from api_v1.serializers import SubscriberSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriber users to be viewed or edited.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

