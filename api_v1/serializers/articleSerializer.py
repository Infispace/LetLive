from rest_framework import serializers
from home.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api_v1:author-detail',
        #queryset=User.objects.filter(is_active=True),
    )
    
    topic = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api_v1:topic-detail',
    )
    
    class Meta:
        model = Article
        fields = '__all__'
        
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:article-detail',
                'lookup_field': 'pk'
            },
        }
