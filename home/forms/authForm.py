"""
:synopsis: Forms for authentication; login and register
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

class RegisterUserForm(forms.ModelForm):
    """
    Register Form with the following fields:
    
    * email
    * username
    * password
    * password 2
    * is_author
    
    `username` and `password` is inherited from `home.forms.LoginForm`
    """
    #: password confirmation field
    password2 = forms.CharField(
      label= 'Retype Password', 
      max_length=25, 
      widget=forms.PasswordInput,
      required=True
    )
    
    #: is_author field to choose between 
    #: `home.models.UserModel.Author` or
    #: `home.models.UserModel.Subcriber`
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
        
        # passwords should match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            msg = "passwords did not match"
            raise forms.ValidationError(msg)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(AuthenticationForm):
    """
    Login Form inherits from `django.contrib.auth.forms.AuthenticationForm`.
    
    Has the following fields:

    * username
    * password
    * keep_loged
    """
    #: keep session login field
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
        
