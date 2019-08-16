from django.forms import ModelForm
from django.contrib.auth.models import User

from home.models import Author, Publisher, Admin

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AppUserForm(ModelForm):
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

class AdminForm(AppUserForm):
    class Meta(AppUserForm.Meta):
        model = Author
        fields = '__all__'
