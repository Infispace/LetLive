from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from home.models import Publisher
from api_v1.serializers import PublisherSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows publisher users to be viewed or edited.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

