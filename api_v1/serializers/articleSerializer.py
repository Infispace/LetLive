from rest_framework import serializers
from home.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api_v1:author-detail',
        #queryset=User.objects.filter(is_active=True),
    )
    
    publisher = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api_v1:publisher-detail',
    )
    
    topic = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api_v1:topic-detail',
    )
    
    class Meta:
        model = Article
        fields = (
          'url',
          'id',
          'author',
          'title',
          'publisher',
          'content',
          'publish_date_time',
          'draft',
          'updated_date_time',
          'created_date_time',
          'topic'
        )
        
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:article-detail',
                'lookup_field': 'pk'
            },
        }
