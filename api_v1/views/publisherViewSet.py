from rest_framework.viewsets import ModelViewSet
from api_v1.serializers import PublisherSerializer
from home.models import Publisher


class PublisherViewSet(ModelViewSet):
    """
    API endpoint that allows publisher users to be viewed or edited.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

