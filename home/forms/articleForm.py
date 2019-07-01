from django.forms import ModelForm
from home.models import Article
from home.models import Topic

class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['content'].label = "Article's Body"
          # title field
          self.fields['title'].label = "Article's Title"
          self.fields['title'].required = True
          self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter the article's tilte",
          })
          # topic field
          self.fields['topic'].label = "Topic Category"
          self.fields['topic'].required = True
          self.fields['topic'].widget.attrs.update({
            'class': 'form-control',
          })
          
    class Meta:
        model = Article
        fields = ['title', 'content', 'topic', 'image']        

class ArticleConfirmForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Article
        fields = ['title']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class TopicDeleteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic_name'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Topic
        fields = ['topic_name']
