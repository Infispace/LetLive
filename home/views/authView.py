from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from ..forms.authForm import LoginForm, RegisterForm
from ..models.userModel import Author

class UserLoginView(generic.TemplateView):
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
            self.form = RegisterForm()
        else:
            self.form = LoginForm()

        return render(request, self.template_name,
            {'next': next, 'form': self.form, 'page': page}
        )

    def signup(self, request):
        success = False
        password = self.form.cleaned_data['password']
        password2 = self.form.cleaned_data['password2']
        password_match = False

        if password != '' and password2 != '' and password == password2:
            password_match = True

        if password_match:
            try:
                author = Author.objects.create_user(
                    username=self.form.cleaned_data['username'],
                    email=self.form.cleaned_data['email'],
                    password=password,
                    user_level= Author.AUTHOR
                )
                success = self.login(request)
                if success:
                    print('success')
            except:
                self.error_string = 'Username already exist. Please try again.'
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


    def post(self, request, next='', page='login', user=None):
        if 'next' in request.POST:
            next = request.POST['next']

        success = False
        if page == 'signup':
            self.form = RegisterForm(request.POST)
            if self.form.is_valid():
                success = self.signup(request);
        else:
            self.form = LoginForm(request.POST)
            if self.form.is_valid():
                success = self.login(request)

        if success and next is not '':
            return HttpResponseRedirect(next)
        elif success:
            return HttpResponseRedirect(reverse('home:index'))

        return render(request, self.template_name,{
            'next': next,
            'form': self.form,
            'page': page,
            'error_string': self.error_string
        })
