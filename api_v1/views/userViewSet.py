from rest_framework.viewsets import ModelViewSet
from api_v1.serializers import UserSerializer
from django.contrib.auth.models import User


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

