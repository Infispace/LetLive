"""
:synopsis: Used to define the views to manage `home.models.userModel.AppUser`
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import TemplateView

from home.forms import RegisterUserForm
from home.forms import DeleteUserForm
from home.models import Publisher
from home.models import Author

class UsersView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        'home.add_publisher',
        'home.delete_publisher',
        'home.delete_author'
    )
    template_name = 'home/users.html'
    authors_list = None
    publisers_list = None
    user_form = None
    user_level = None
    error_string = ''

    def set_user_level(self, user_level):
        if user_level == 'publisher':
            self.user_level = Publisher.PUBLISHER
        elif user_level == 'author':
            self.user_level = Author.AUTHOR
        else:
            self.user_level = user_level

    def get(self, request, page, users='list', user_level='all', user_id=0):
        self.set_user_level(user_level)

        if page == 'user_delete'and user_id != 0:
            user_delete = get_object_or_404(User, pk=user_id)
            user_delete_form = DeleteUserForm(instance=user_delete)
            return render(request, self.template_name, {
                'page': page,
                'user_delete': user_delete,
                'form': user_delete_form,
            })
        elif users == 'new':
            self.user_form = RegisterUserForm()
        else:
            self.authors_list = User.objects.filter(
                groups=Group.objects.get(name='Authors')
            )
            self.publisers_list = User.objects.filter(
                groups=Group.objects.get(name='Publishers')
            )

        return render(request, self.template_name, {
            'page': page,
            'users': users,
            'user_level': self.user_level,
            'authors_list': self.authors_list,
            'publishers_list': self.publisers_list,
            'user_form': self.user_form
        })

    def add_publisher(self):
        saved = False
        if self.user_form.is_valid():
            password = self.user_form.cleaned_data['password']
            password2 = self.user_form.cleaned_data['password2']

            password_match = False
            if password != '' and password2 != '' and password == password2:
                password_match = True

            if password_match:
                try:
                    publisher = Publisher.objects.create_user(
                        username=self.user_form.cleaned_data['username'],
                        email=self.user_form.cleaned_data['email'],
                        password=password,
                        user_level= Publisher.PUBLISHER
                    )
                    saved = True
                except:
                    self.error_string = 'Username already exist. Please try again.'
            else:
                self.error_string = "Passwords do not match."

        return saved

    def post(self, request, page, users='list', user_level='all', user_id=0):
        self.set_user_level(user_level)

        success = False
        if page == 'user_delete' and user_id != 0:
            error_string = ''
            user = get_object_or_404(User, pk=user_id)
            user_delete_form = DeleteUserForm(request.POST, instance=user)
            if user_delete_form.is_valid():
                user_delete = get_object_or_404(
                    User,
                    username=user_delete_form.cleaned_data['username']
                )
                user_delete.delete()
                return HttpResponseRedirect(reverse('home:users_default'))
            else:
                return render(request, self.template_name, {
                    'page': page,
                    'user_delete': user_delete,
                    'form': user_delete_form,
                    'error_string': error_string,
                })
        elif users == 'new':
            self.user_form = RegisterUserForm(request.POST)
            success = self.add_publisher()

        if success:
            return HttpResponseRedirect(reverse('home:users_default'))
        else:
            return render(request, self.template_name, {
                'page': page,
                'users': users,
                'user_form': self.user_form,
                'error_string': self.error_string,
            })
