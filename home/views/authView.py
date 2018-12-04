from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views import generic

from ..forms.authForm import LoginForm, RegisterForm

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

    def post(self, request, next='', page='login', user=None):
        if 'next' in request.POST:
            next = request.POST['next']

        if page == 'signup':
            self.form = RegisterForm(request.POST)
            if self.form.is_valid():
                # create user in author's group
                if False:
                    if next is not '':
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect(reverse('home:user_default'))
                else:
                    #self.error_string = 'Email and/or username already exist. Please try again.'
                    self.error_string = "We don't accept new users at this time."

            return render(request, self.template_name,{
                'next': next,
                'form': self.form,
                'page': page,
                'error_string': self.error_string
            })

        else:
            self.form = LoginForm(request.POST)
            if self.form.is_valid():
                user = authenticate(username=self.form.cleaned_data['username'],
                    password= self.form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    if next is not '':
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect(reverse('home:index'))
                else:
                    self.error_string = "Your username and password didn't match. Please try again."

            return render(request, self.template_name,{
                'next': next,
                'form': self.form,
                'page': page,
                'error_string': self.error_string
            })
