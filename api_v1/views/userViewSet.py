from rest_framework import viewsets
from rest_framework import generics
from api_v1.serializers import UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #: The queryset to beg objects.
    queryset = User.objects.all().order_by('-date_joined')
    #: The serializer to user.
    serializer_class = UserSerializer

