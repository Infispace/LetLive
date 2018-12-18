from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterUserForm(ModelForm):
    password2 = forms.CharField(label='Retype Password', max_length=25, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean(self):
        super().clean()
        validate_password(self.cleaned_data.get("password"))

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=50)
    password = forms.CharField(label='Password', max_length=25, widget=forms.PasswordInput)

class DeleteUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})
        
    class Meta:
        model = User
        fields = ['username']
