from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterUserForm(ModelForm):
    password2 = forms.CharField(
      label='Retype Password', 
      max_length=25, 
      widget=forms.PasswordInput,
      required=True
    )
    
    is_author = forms.BooleanField(
      label ='Register as an author', 
      required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_author'].widget = forms.HiddenInput()

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
    username = forms.CharField(
      label='User Name', 
      max_length=50, 
      required=True
    )
   
    password = forms.CharField(
      label='Password', 
      max_length=25, 
      widget=forms.PasswordInput, 
      required=True
    )   

class DeleteUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})

    class Meta:
        model = User
        fields = ['username']
