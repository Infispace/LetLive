"""
:synopsis: Forms Efiting Articles and topics
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from .bootstrapForm import BootstrapForm

class RegisterUserForm(UserCreationForm, BootstrapForm):
    """
    Register Form inherits from `django.contrib.auth.forms.UserCreationForm`
    
    Has the following fields:
    
    * email
    * username
    * password1
    * password2
    * is_author
    """
    #: Email field for new user email
    email = forms.EmailField()
    
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
        self.add_form_control(self.fields)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
           'email', 
           'username',
        ]

class LoginForm(AuthenticationForm, BootstrapForm):
    """
    Login form inherits from `django.contrib.auth.forms.AuthenticationForm`.
    
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
        self.add_form_control(self.fields)
        self.fields['keep_loged'].widget = forms.HiddenInput()

class PasswordResetForm(PasswordResetForm, BootstrapForm):
    """
    Password reset form inherits from `django.contrib.auth.forms.PasswordResetForm`.
    
    Has the following fields:

    * email
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control(self.fields)

class PasswordChangeForm(PasswordChangeForm, BootstrapForm):
    """
    Password change form inherits from `django.contrib.auth.forms.PasswordChangeForm`.
    
    Has the following fields:

    * old_password
    * new_password1
    * new_password2
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control(self.fields)
