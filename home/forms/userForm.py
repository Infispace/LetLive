from django import forms
from django.contrib.auth.models import User
from home.models import Author
from home.models import Publisher
from home.models import Subscriber
from home.models import Admin

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AppUserForm(forms.ModelForm):
    class Meta:
        exclude = ['user', 'user_level']

class AuthorForm(AppUserForm):
    class Meta(AppUserForm.Meta):
        model = Author
        fields = '__all__'

class PublisherForm(AppUserForm):
    class Meta(AppUserForm.Meta):
        model = Author
        fields = '__all__'

class SubscriberForm(AppUserForm):
    class Meta(AppUserForm.Meta):
        model = Subscriber
        exclude = ['user', 'user_level', 'subscription_type']
        
class AdminForm(AppUserForm):
    class Meta(AppUserForm.Meta):
        model = Author
        fields = '__all__'

class DeleteUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})

    class Meta:
        model = User
        fields = ['username']

