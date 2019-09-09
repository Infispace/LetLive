from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework import generics
from home.models import Article
from api_v1.serializers import ArticleSerializer
from api_v1.permissions import IsOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        DjangoModelPermissionsOrAnonReadOnly,
        IsOwnerOrReadOnly,
    ]

