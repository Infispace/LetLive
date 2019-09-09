"""
:synopsis: View for making subscription by the authenticated user.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.urls import reverse
from django.conf import settings
from home.forms import UserGroupForm
from home.models import AppUser
from home.models import Author
from home.models import Subscriber
from home.models import change_user_groups


class SubscriptionView(LoginRequiredMixin, TemplateView):
    """
    Class for user profile
    """
    #: The html template to render.
    template_name = 'home/account_templates/account_base.html'
    #: The authenticated user.
    view_user = None
    #: The html form to edit user groups
    group_form = None
    #: The errors found
    error_string = None
    #: The data for the user groups
    group_data = None
    

    def get_group_data(self):
        """
        Get the user groups and set the form data
        """
        self.group_data = {
            'groups': [],
        }

        try:
          self.request.user.author
          self.group_data['groups'].append(AppUser.AUTHOR)
        except ObjectDoesNotExist:
            pass

        try:
          self.request.user.subscriber
          self.group_data['groups'].append(AppUser.SUBSCRIBER)
        except ObjectDoesNotExist:
            pass

        try:
          self.request.user.admin
          self.group_data['groups'].append(AppUser.ADMIN)
        except ObjectDoesNotExist:
            pass

    def save_user_group(self):
        """
        Save the user groups.
        """
        change_user_groups(
            self.request.user, 
            self.group_form.cleaned_data['groups']
        )

    def get(self, request, *args, **kwargs):
        """
        Called when HTTP GET method is used.
        Displays the edit user profile form.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        """
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # set form to display
        self.get_group_data()
        self.group_form = UserGroupForm(initial=self.group_data)

        # render template
        return render(request, self.template_name, {
            'page': page,
            'group_form': self.group_form,
        })

    def post(self, request, *args, **kwargs):
        """
        Called when HTTP POST method is used.
        Edits the user profile from the form data.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        """
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # get forms data
        self.get_group_data()
        self.group_form = UserGroupForm(
            request.POST, 
            initial=self.group_data
        )
        
        # save
        saved = False
        try:
            if self.group_form.is_valid():
                self.save_user_group()
                saved = True

        except Exception as e:
            saved = False
            self.error_string = 'There was an error. Please try again.' 
            if settings.DEBUG:
                self.error_string = e
        
        # render template
        if saved:
            return HttpResponseRedirect(reverse('home:user_profile'))

        return render(request, self.template_name, {
            'page': page,
            'group_form': self.group_form,
            'error_string': self.error_string,
        }, status=400)

