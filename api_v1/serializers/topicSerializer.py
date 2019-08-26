from rest_framework import serializers
from home.models import Topic


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    parent_topic = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name='api_v1:topic-detail',
    )
    
    #sub_topics = self.__init__(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = '__all__'
        
        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:topic-detail',
                'lookup_field': 'pk'
            },
        }

