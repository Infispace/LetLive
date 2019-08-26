from rest_framework.viewsets import ModelViewSet
from api_v1.serializers import SubscriberSerializer
from home.models import Subscriber


class SubscriberViewSet(ModelViewSet):
    """
    API endpoint that allows subscriber users to be viewed or edited.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

