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
from django.views.generic import TemplateView
from home.forms import UserForm
from home.forms import AuthorForm
from home.forms import PublisherForm
from home.forms import AdminForm

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Class for user profile
    """
    #: The html template to render.
    template_name = 'home/account.html'
    #: The authenticated user.
    view_user = None
    #: The html form to render
    form = None
    #: form for the user model
    user_form = None

    def set_form(self, user, request=None):
        """
        Initialize the form to use to edit user profile.
        """
        try:
            user.author
            if request is not None:
                self.form = AuthorForm(request.POST, instance=user.author)
            else:
                self.form = AuthorForm(instance=user.author)
        except ObjectDoesNotExist:
            pass

        try:
            user.publisher
            if request is not None:
                self.form = PublisherForm(request.POST, instance=user.publisher)
            else:
                self.form = PublisherForm(instance=user.publisher)
        except ObjectDoesNotExist:
            pass

        try:
            user.admin
            if request is not None:
                self.form = AdminForm(request.POST, instance=user.admin)
            else:
                self.form = AdminForm(instance=user.admin)
        except ObjectDoesNotExist:
            pass

    def get(self, request, page):
        """
        Called when HTTP GET method is used.
        Displays the edit user profile form.
        """
        # set forms and user to display
        self.view_user = request.user        
        if(page == 'user_profile_edit'):
          self.set_form(self.view_user)
          self.user_form = UserForm(instance=self.view_user)
        
        # render template
        return render(request, self.template_name, {
            'view_user': self.view_user,
            'form_user': self.user_form,
            'form_profile': self.form,
            'page': page,
        })

    def post(self, request, page):
        """
        Called when HTTP POST method is used.
        Edits the user profile from the form data.
        """
        # only allow for user_profile_edit url
        if(page != 'user_profile_edit'):
            raise PermissionDenied
        
        # get form data    
        self.user_form = UserForm(request.POST, instance=request.user)
        self.set_form(request.user, request)
        saved = False

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

        # render template
        if saved:
            return HttpResponseRedirect(reverse('home:user_profile'))
        else:
          return render(request, self.template_name, {
              'form_user': self.user_form,
              'form_profile': self.form,
              'error_string': 'Check the following form errors!',
              'page': page,
          })
