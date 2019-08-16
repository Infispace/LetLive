from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from home.models import Author
from api_v1.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows author users to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

