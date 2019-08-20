"""
:synopsis: Used for authenticating the users.
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

class UserLoginView(TemplateView):
    """
    Class for authenticating users.
    Used for login and registering users.
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
        Renders the authentication forms.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest        
        :param str next: the next url after HTTP POST
        :param str page: the page to render, default is 'login'
        :return: renders the html template
        :rtype: django.shortcuts.render
        """
        if 'next' in request.GET:
            next = request.GET['next']

        if request.user.is_authenticated:
            if next != '':
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('home:index'))

        if page == 'signup':
            self.form = RegisterUserForm()
        else:
            self.form = LoginForm()

        return render(request, self.template_name,{
            'next': next, 
            'form': self.form, 
            'page': page
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
        password = self.form.cleaned_data['password']
        password2 = self.form.cleaned_data['password2']
        is_author = self.form.cleaned_data['is_author']
        
        user_level = AppUser.SUBSCRIBER
        if is_author:
            user_level = AppUser.AUTHOR

        if password != '' and password2 != '' and password == password2:
            try:
                if is_author:
                    Author.objects.create_user(
                        username=self.form.cleaned_data['username'],
                        email=self.form.cleaned_data['email'],
                        password=password,
                        user_level= user_level
                    )
                else:
                    Subscriber.objects.create_user(
                        username=self.form.cleaned_data['username'],
                        email=self.form.cleaned_data['email'],
                        password=password,
                        user_level= user_level
                    )
                    
                success = self.login(request)
            except Exception as e:
                self.error_string = 'There was an error. Please try again.'
                #self.error_string = e
                
        else:
            self.error_string = "Passwords do not match."

        return success

    def login(self, request):
        """
        Authenticates the user using the form data.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :return: True or False
        :rtype: bool
        """
        success = False
        user = authenticate(
            username=self.form.cleaned_data['username'],
            password= self.form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            success = True
        else:
            self.error_string = "Your username and/or password didn't match. Please try again."

        return success

    def post(self, request, next='', page='login'):
        """
        Called if HTTP POST is requested.
        Either creates a new user or authenticate an existing user.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param str next: the next url after HTTP POST
        :param str page: the page to render, default is 'login'
        :return: renders the html template
        :rtype: django.shortcuts.render
        """
        if 'next' in request.POST:
            next = request.POST['next']

        success = False
        errors = []
        if page == 'signup':
            self.form = RegisterUserForm(request.POST)
            if self.form.is_valid():
                success = self.signup(request);
        else:
            self.form = LoginForm(request.POST)
            if self.form.is_valid():
                success = self.login(request)
                if self.form.cleaned_data['keep_loged']:
                    request.session['user'] = {
                        'keep_loged': 'true'
                    }

        if success and next is not '':
            return HttpResponseRedirect(next)
        elif success:
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return render(request, self.template_name,{
                'next': next,
                'form': self.form,
                'page': page,
                'error_string': self.error_string,
            })
