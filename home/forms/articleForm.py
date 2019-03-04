from django import forms
from ..models import Article
from ..models import Topic

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'topic', 'image']

class ArticleConfirmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Article
        fields = ['title']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class TopicDeleteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic_name'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Topic
        fields = ['topic_name']
