"""
:synopsis: Used for Registering new users.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.db import transaction
from home.forms import LoginForm
from home.forms import RegisterUserForm
from home.models import AppUser
from home.models import Author
from home.models import Subscriber

class UserRegistrationView(TemplateView):
    """
    Class for registering new users and authenticating them.
    """
    #: The html template to render.
    template_name = 'home/login.html'
    #: The html form to render
    form = None
    #: The error string if an error occurs
    error_string = ''

    def get(self, request, next='', page='login'):
        """
        Called if HTTP GET is requested.
        Renders the registration form.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest        
        :param str next: the next url after HTTP POST
        :param str page: the page to render, default is 'login'
        :return: renders the html template
        :rtype: django.shortcuts.render
        """
        # get next page url
        if 'next' in request.GET:
            next = request.GET['next']

        # redirect authenticated users
        if request.user.is_authenticated:
            if next != '':
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('home:index'))

        # set form to render
        self.form = RegisterUserForm()

        # render the template
        return render(request, self.template_name,{
            'next': next, 
            'form': self.form, 
            'page': page
        })

    def post(self, request, next='', page='login'):
        """
        Called if HTTP POST is requested.
        Creates a new user.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param str next: the next url after HTTP POST
        :param str page: the page to render, default is 'login'
        :return: renders the html template
        :rtype: django.shortcuts.render
        """
        # get next page url
        if 'next' in request.POST:
            next = request.POST['next']

        # register new user
        success = False
        try: 
            self.form = RegisterUserForm(request.POST)
            success = self.signup(request)
        except Exception as e:
            self.error_string = 'There was an error. Please try again.' 
            #self.error_string = e #for debug

        # render template
        if success and next is not '':
            return HttpResponseRedirect(next)
        elif success:
            return HttpResponseRedirect(reverse('home:user_login'))
        else:
            return render(request, self.template_name,{
                'next': next,
                'form': self.form,
                'page': page,
                'error_string': self.error_string,
            })

    @transaction.atomic
    def signup(self, request):
        """
        Creates a new user.
        The new user is either `SUBSCRIBER` or `AUTHOR`
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :return: True or False
        :rtype: bool
        """
        success = False
        if self.form.is_valid():
            # create new user
            user = self.form.save()
            
            # set user level of the new user
            user_level = AppUser.SUBSCRIBER
            if self.form.cleaned_data['is_author']:
                success = Author.objects.create(
                    user=user, 
                    user_level=AppUser.AUTHOR
                )
            else:
                success = Subscriber.objects.create(
                    user=user, 
                    user_level=AppUser.SUBSCRIBER
                )

        return success

