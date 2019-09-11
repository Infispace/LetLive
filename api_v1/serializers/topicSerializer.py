from rest_framework import serializers
from django.db import transaction
from django.urls import reverse
from home.models import Topic


class SubTopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ['url', 'topic_name', 'intro']

        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:topic-detail',
                'lookup_field': 'pk'
            },
        }

class TopicSerializer(serializers.HyperlinkedModelSerializer):
    parent_topic = serializers.HyperlinkedRelatedField(
        many=False,
        default=None,
        required=False,
        allow_null=True,
        queryset=Topic.objects.all(),
        view_name='api_v1:topic-detail',
    )

    sub_topics = SubTopicSerializer(
        many=True, 
        default=None,
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = Topic
        fields = '__all__'

        extra_kwargs = {
            'url': {
                'view_name': 'api_v1:topic-detail',
                'lookup_field': 'pk'
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        sub_topics = validated_data.pop('sub_topics')
        topic = Topic.objects.create(**validated_data)
        
        if sub_topics is not None:
            for topic_data in sub_topics:
                Topic.objects.create(parent_topic=topic, **topic_data)
        
        return topic

