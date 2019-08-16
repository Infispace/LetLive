from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterUserForm(forms.ModelForm):
    password2 = forms.CharField(
      label= 'Retype Password', 
      max_length=25, 
      widget=forms.PasswordInput,
      required=True
    )
    
    is_author = forms.BooleanField(
      label = 'Register as an author', 
      required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_author'].widget = forms.HiddenInput()
        self.fields['is_author'].widget.attrs.update({
          'class': 'form-check-input',
        })
        self.fields['password2'].widget.attrs.update({
          'class': 'form-control',
        })
        self.fields['username'].widget.attrs.update({
          'class': 'form-control',
        })
        self.fields['password'].widget.attrs.update({
          'class': 'form-control',
        })
        self.fields['username'].widget.attrs.update({
          'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
          'class': 'form-control',
        })     

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
      label='Username', 
      max_length=50, 
      required=True
    )
   
    password = forms.CharField(
      label='Password', 
      max_length=25, 
      widget=forms.PasswordInput, 
      required=True
    )   
    
    keep_loged = forms.BooleanField(
      label = 'Remember me', 
      required=False,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
          'class': 'form-control',
        })
        self.fields['password'].widget.attrs.update({
          'class': 'form-control',
        })

class DeleteUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})

    class Meta:
        model = User
        fields = ['username']
