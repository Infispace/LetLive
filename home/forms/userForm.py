"""
:synopsis: Forms for editing the `User` and `AppUser` details
"""
from django import forms
from django.contrib.auth.models import User
from home.models import Author
from home.models import Publisher
from home.models import Subscriber
from home.models import Admin
from .bootstrapForm import BootstrapForm

class UserForm(forms.ModelForm, BootstrapForm):
    """
    Form to edit `django.contrib.auth.models.User` model.
    
    Has the following fields:

    * first_name
    * last_name
    * email
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control(self.fields)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AppUserForm(forms.ModelForm, BootstrapForm):
    """
    Virtual form to edit virtual model `home.models.AppUser`.
    
    Inherited by other forms. It is not used directly.
    
    Has the following fields:

    * telephone
    * address
    * avatar
    * dob
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget = forms.HiddenInput()
        self.fields['dob'].label = 'Date of birth'
        self.fields['dob'].widget.input_type = 'date'
        self.add_form_control(self.fields)

    class Meta:
        exclude = ['user']

class AuthorForm(AppUserForm):
    """
    Form to edit `home.models.Author` model.
    
    Inherits `home.forms.AppUserForm` form.
    """
    class Meta(AppUserForm.Meta):
        model = Author
        exclude = ['user', 'author_type']

class PublisherForm(AppUserForm):
    """
    Form to edit `home.models.Publisher` model.
    
    Inherits `home.forms.AppUserForm` form.
    """
    class Meta(AppUserForm.Meta):
        model = Author
        fields = '__all__'

class SubscriberForm(AppUserForm):
    """
    Form to edit `home.models.Subscriber` model.
    
    Inherits `home.forms.AppUserForm` form.
    """
    class Meta(AppUserForm.Meta):
        model = Subscriber
        exclude = ['user', 'subscription_type']

class AdminForm(AppUserForm):
    """
    Form to edit `home.models.Admin` model.
    
    Inherits `home.forms.AppUserForm` form.
    """
    class Meta(AppUserForm.Meta):
        model = Admin
        fields = '__all__'

class DeleteUserForm(forms.ModelForm):
    """
    Form to delete `django.contrib.auth.models.User` model.
    
    Has the following fields:

    * username
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'readonly': True})

    class Meta:
        model = User
        fields = ['username']

