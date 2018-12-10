from django import forms
from ..models.articleModel import Article
from ..models.topicModel import Topic

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'publisher', 'publish_date']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
