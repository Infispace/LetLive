from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from home.models import Subscriber
from home.models import Author
from home.models import Publisher
from home.models import Admin
from api_v1.serializers import UserSerializer
from api_v1.serializers import SubscriberSerializer
from api_v1.serializers import AuthorSerializer
from api_v1.serializers import PublisherSerializer
from api_v1.serializers import AdminSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriber users to be viewed or edited.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    
class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows author users to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
class PublisherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows publisher users to be viewed or edited.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    
class AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin users to be viewed or edited.
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
