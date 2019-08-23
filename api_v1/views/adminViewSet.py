from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet 
from api_v1.serializers import AdminSerializer
from home.models import Admin


class AdminViewSet(ModelViewSet):
    """
    API endpoint that allows admin users to be viewed or edited.
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
