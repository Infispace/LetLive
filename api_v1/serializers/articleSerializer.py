from rest_framework import serializers
from home.models import Article
from home.models import Author
from home.models import Topic


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api_v1:author-detail',
    )
    
    topic = serializers.HyperlinkedRelatedField(
        many=False,
        queryset=Topic.objects.all(),
        view_name='api_v1:topic-detail',
    )
    
    def create(self, validated_data, *args, **kwargs):
        author = self.context['request'].user.author

        return Article.objects.create(
            author=author,
            **validated_data
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
