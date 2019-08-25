"""
:synopsis: Forms for viewing and modifying `home.models.Article` and `home.models.Topic`
"""
from django.forms import ModelForm
from home.models import Article
from home.models import Topic
from .bootstrapForm import BootstrapForm

class ArticleForm(ModelForm, BootstrapForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.add_form_control(self.fields)
          self.fields['content'].label = "Article's Body"
          self.fields['title'].label = "Article's Title"
          self.fields['title'].required = True
          self.fields['topic'].label = "Topic Category"
          self.fields['topic'].required = True

    class Meta:
        model = Article
        fields = ['title', 'content', 'topic', 'image']        

class ArticleConfirmForm(ModelForm, BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control(self.fields)
        self.fields['title'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Article
        fields = ['title']

class TopicForm(ModelForm, BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control(self.fields)
        
    class Meta:
        model = Topic
        fields = '__all__'

class TopicDeleteForm(ModelForm, BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control(self.fields)
        self.fields['topic_name'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Topic
        fields = ['topic_name']
