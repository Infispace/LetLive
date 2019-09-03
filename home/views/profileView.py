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
from home.forms import SubscriberForm
from home.forms import AdminForm

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Class for user profile
    """
    #: The html template to render.
    template_name = 'home/account_templates/account_base.html'
    #: The authenticated user.
    view_user = None
    #: The html form to edit Admin Profile
    admin_form = None
    #: The html form for edit Author Profile
    author_form = None
    #: The html form for edit Subscriber Profile
    subscriber_form = None
    #: form for the user model
    user_form = None
    #: The errors found
    error_string = None

    def set_profile_forms(self):
        """
        Initialize the form to use to edit user profile.
        """
        author_instance = None
        subscriber_instance = None
        admin_instance = None
        user_form_class = None
        
        try:
            author_instance = self.request.user.author
            self.author_form = AuthorForm(instance=author_instance)
        except ObjectDoesNotExist:
            pass

        try:
            subscriber_instance = self.request.user.subscriber
            self.subscriber_form = SubscriberForm(instance=subscriber_instance)
        except ObjectDoesNotExist:
            pass

        try:
            admin_instance = self.request.user.admin
            self.admin_form = AdminForm(instance=admin_instance)
        except ObjectDoesNotExist:
            pass

        # set the profile forms for editing
        if self.request.method == 'POST':
            self.author_form = user_form_class(
                self.request.POST,
                instance=author_instance
            )

            self.subscriber_form = user_form_class(
                self.request.POST,
                instance=subscriber_instance
            )

            self.admin_form = user_form_class(
                self.request.POST,
                instance=admin_instance
            )


    def save_profile_forms(self):
        # save User model attributes
        if self.user_form.has_changed():
            if self.user_form.is_valid():
                self.user_form.save()

        #: save the profile data
        if self.admin_form != None:
            if self.admin_form.has_changed() and self.admin_form.is_valid():
                self.admin_form.save()
            
        if self.subscriber_form != None:
            if self.subscriber_form.has_changed() and self.subscriber_form.is_valid():
                self.subscriber_form.save()
                
        if self.author_form != None:
            if self.author_form.has_changed() and self.author_form.is_valid():
                self.author_form.save()


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
        if page == 'user_profile_edit' or page == 'user_account_edit':
          self.set_profile_forms()
          self.user_form = UserForm(instance=self.view_user)
        
        # render template
        return render(request, self.template_name, {
            'view_user': self.view_user,
            'user_form': self.user_form,
            'admin_form': self.admin_form,
            'author_form': self.author_form,
            'subscriber_form': self.subscriber_form,
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
        
        # form data    
        self.user_form = UserForm(request.POST, instance=request.user)
        self.set_profile_forms()
        
        # save form data
        saved = False
        try:
            save_profile_forms()
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
              'user_form': self.user_form,
              'form_profile': self.form,
              'error_string': self.error_string,
              'page': page,
          }, status=400)
