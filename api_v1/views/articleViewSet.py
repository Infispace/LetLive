from rest_framework import viewsets
from rest_framework import generics
from home.models import Article
from api_v1.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer

