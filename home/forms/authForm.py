"""
:synopsis: Forms Efiting Articles and topics
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import forms as auth_forms
from .bootstrapForm import BootstrapForm

class RegisterUserForm(auth_forms.UserCreationForm, BootstrapForm):
    """
    Register Form inherits from `django.contrib.auth.forms.UserCreationForm`
    
    Has the following fields:
    
    * email
    * username
    * password1
    * password2
    """
    #: Email field for new user email
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = [
           'email', 
           'username',
        ]

class LoginForm(auth_forms.AuthenticationForm, BootstrapForm):
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
        self.add_form_control()
        self.fields['keep_loged'].widget = forms.HiddenInput()
        self.fields['username'].label = 'Username/ Email'

class PasswordResetForm(auth_forms.PasswordResetForm, BootstrapForm):
    """
    Password reset form inherits from `django.contrib.auth.forms.PasswordResetForm`.
    
    Has the following fields:

    * email
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

class PasswordChangeForm(auth_forms.PasswordChangeForm, BootstrapForm):
    """
    Password change form inherits from `django.contrib.auth.forms.PasswordChangeForm`.
    
    Has the following fields:

    * old_password
    * new_password1
    * new_password2
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

class SetPasswordForm(auth_forms.SetPasswordForm, BootstrapForm):
    """
    Password change form inherits from `django.contrib.auth.forms.SetPasswordForm`.
    
    Has the following fields:

    * new_password1
    * new_password2
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

