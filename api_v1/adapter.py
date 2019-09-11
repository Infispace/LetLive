from django.conf import settings
from django.urls import reverse
from allauth.utils import build_absolute_uri
from allauth.account.adapter import DefaultAccountAdapter

class ApiAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Constructs the email confirmation (activation) url.
        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "home:account_confirm_email",
            args=[emailconfirmation.key]
        )

        ret = build_absolute_uri(request, url)

        return ret
