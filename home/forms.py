from django import forms
from .models import Article

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    username = forms.CharField(label='User Name', max_length=50)
    password = forms.CharField(label='Password', max_length=25, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Retype Password', max_length=25, widget=forms.PasswordInput)

class LoginForm(RegisterForm):
    email = None
    password2 = None

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
