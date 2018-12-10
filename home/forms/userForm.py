from django import forms
from django.contrib.auth.models import User

from ..models.userModel import Author, Publisher, Admin

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_login', 'username', 'first_name', 'last_name', 'email')

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

class AdminForm(AppUserForm):
    class Meta(AppUserForm.Meta):
        model = Author
        fields = '__all__'
