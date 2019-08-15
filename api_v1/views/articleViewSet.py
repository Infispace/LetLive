from rest_framework import viewsets
from rest_framework import generics
from home.models import Article
from home.models import Topic
from api_v1.serializers import ArticleSerializer
from api_v1.serializers import TopicSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer
    
class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows topics to be viewed or edited.
    """
    queryset = Topic.objects.all().order_by('id')
    serializer_class = TopicSerializer

