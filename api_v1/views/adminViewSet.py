from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from home.models import Admin
from api_v1.serializers import AdminSerializer


class AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin users to be viewed or edited.
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
