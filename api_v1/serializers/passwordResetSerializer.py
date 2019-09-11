from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import serializers


# Get the UserModel
UserModel = get_user_model()

class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'email_template_name': 
                'home/email/password_reset_email.txt',
            
            'html_email_template_name': 
                'home/email/password_reset_email.html',
        }
        self.reset_form.save(**opts)

