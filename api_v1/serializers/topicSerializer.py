from rest_framework import serializers
from home.models import Topic


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    parent_topic = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name='api_v1:topic-detail',
    )
    
    class Meta:
        model = Topic
        fields = (
          'url',
          'id',
          'topic_name',
          'intro',
          'parent_topic'
        )
        
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:topic-detail',
                'lookup_field': 'pk'
            },
        }

