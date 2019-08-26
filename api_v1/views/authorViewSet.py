from rest_framework.viewsets import ModelViewSet
from api_v1.serializers import AuthorSerializer
from home.models import Author


class AuthorViewSet(ModelViewSet):
    """
    API endpoint that allows author users to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

