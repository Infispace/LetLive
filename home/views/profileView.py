"""
:synopsis: View and edit authenticated user profile
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView
from home.forms import UserForm
from home.forms import AuthorForm
from home.forms import PublisherForm
from home.forms import SubscriberForm
from home.forms import AdminForm

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Class for user profile
    """
    #: The html template to render.
    template_name = 'home/account.html'
    #: The authenticated user.
    view_user = None
    #: The html form for AppUser Profile to render
    form = None
    #: form for the user model
    user_form = None
    #: The errors found
    error_string = None

    def set_form(self):
        """
        Initialize the form to use to edit user profile.
        """
        user_instance = None
        user_form_class = None
        try:
            user_instance = self.request.user.author
            user_form_class = AuthorForm
        except ObjectDoesNotExist:
            pass

        try:
            user_instance = self.request.user.publisher
            user_form_class = PublisherForm
        except ObjectDoesNotExist:
            pass

        try:
            user_instance = self.request.user.subscriber
            user_form_class = SubscriberForm
        except ObjectDoesNotExist:
            pass

        try:
            user_instance = self.request.user.admin
            user_form_class = AdminForm
        except ObjectDoesNotExist:
            pass

        # return if no profile is found
        if not user_instance:
            return

        # set profile form
        if self.request.method == 'POST':
            self.form = user_form_class(
                self.request.POST,
                instance=user_instance
            )
        else:
            self.form = user_form_class(instance=user_instance)

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
        
        # set forms and user to display
        self.view_user = request.user        
        if(page == 'user_profile_edit'):
          self.set_form()
          self.user_form = UserForm(instance=self.view_user)
        
        # render template
        return render(request, self.template_name, {
            'view_user': self.view_user,
            'form_user': self.user_form,
            'form_profile': self.form,
            'page': page,
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
        
        # only allow for user_profile_edit url
        if(page != 'user_profile_edit'):
            raise PermissionDenied
        
        # get form data    
        self.user_form = UserForm(request.POST, instance=request.user)
        self.set_form()
        saved = False

        try:
            # save User model attributes
            if self.user_form.has_changed():
                if self.user_form.is_valid():
                    self.user_form.save()
                    saved = True

            #: save AppUser model attributes
            if self.form.has_changed():
                if self.form.is_valid():
                    self.form.save()
                    saved = True
        except Exception as e:
            saved = False
            self.error_string = 'There was an error. Please try again.' 
            if settings.DEBUG:
                self.error_string = e

        # render template
        if saved:
            return HttpResponseRedirect(reverse('home:user_profile'))
        else:
          return render(request, self.template_name, {
              'form_user': self.user_form,
              'form_profile': self.form,
              'error_string': self.error_string,
              'page': page,
          }, status=400)
