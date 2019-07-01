from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.db import transaction

from home.forms import LoginForm, RegisterUserForm
from home.models import AppUser, Author, Subscriber

@login_required()
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return HttpResponse('Unknown Error')

class UserLoginView(TemplateView):
    template_name = 'home/login.html'
    form = None
    error_string = ''

    def get(self, request, page='login', next=''):
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

        return render(request, self.template_name,
            {'next': next, 'form': self.form, 'page': page}
        )

    @transaction.atomic
    def signup(self, request):
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

        return render(request, self.template_name,{
            'next': next,
            'form': self.form,
            'page': page,
            'error_string': self.error_string,
        })
