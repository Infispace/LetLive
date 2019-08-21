"""
:synopsis: Used to define the views to manage users
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import TemplateView
from home.forms import RegisterUserForm
from home.forms import DeleteUserForm
from home.models import Publisher
from home.models import Author

class UsersView(PermissionRequiredMixin, TemplateView):
    """
    Class to manage users. Add and delete users. 
    Admins only can access this view.
    """
    #: The permissions required to access the view
    permission_required = (
        'home.add_publisher',
        'home.delete_publisher',
        'home.delete_author'
    )
    #: The html template to render
    template_name = 'home/users.html'
    #: The list of users with author user level
    authors_list = None
    #: The list of users with publisher user level
    publisers_list = None
    #: The form to render
    user_form = None
    #: The error to be displayed
    error_string = ''
    #: The user to view or edit
    view_user = None

    def get(self, request, page, user_id=0):
        """
        Display users list with filters `/authors/` and `/publishers/`.
        
        Shows A specific users filtered with `/pk/`.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param str page: the page to render, default is 'login'
        :param int user_id: the user id to filter
        """
        # get user list or user with pk
        if user_id == 0:
            self.authors_list = User.objects.filter(
                groups=Group.objects.get(name='Authors')
            )
            self.publisers_list = User.objects.filter(
                groups=Group.objects.get(name='Publishers')
            )
        else :
            self.view_user = get_object_or_404(User, pk=user_id)
            
        # set form to render
        if page == 'user_delete':
            self.user_form = DeleteUserForm(instance=self.view_user)
        elif page == 'user_new':
            self.user_form = RegisterUserForm()

        # render template
        if page == 'user_view':
            self.template_name = 'home/account.html'
        
        return render(request, self.template_name, {
            'page': page,
            'authors_list': self.authors_list,
            'publishers_list': self.publisers_list,
            'user_form': self.user_form,
            'view_user': self.view_user,
        })

    def post(self, request, page, user_id=0):
        """
        Creates a new user `/new/`.
        
        Edit a specific users filtered with `/pk/`
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param str page: the page to render, default is 'login'
        :param int user_id: the user id to filter
        """
        # restrict to new and delete
        permited = False;
        if page == 'user_new' or page == 'user_delete':
            permited = True;

        if not permited:
            raise PermissionDenied

        # get user from user_id
        if user_id != 0:
            self.view_user = get_object_or_404(User, pk=user_id)
        
        # get form to validate
        if page == 'user_new':
            self.user_form = RegisterUserForm(request.POST)
        elif page == 'user_delete':
            self.user_form = DeleteUserForm(
                request.POST, instance=self.view_user
            )
        
        # make db edits
        success = self.user_form.is_valid()
        
        print(success, self.user_form, self.view_user)
        
        if success and page == 'user_delete':
            self.view_user.delete()
            success = True
        elif success and page == 'user_new':
            success = self.add_user('')
        
        # render template
        if success:
            return HttpResponseRedirect(reverse('home:user_default'))
        else:
            return render(request, self.template_name, {
                'page': page,
                'view_user': self.view_user,
                'user_form': self.user_form,
                'error_string': self.error_string,
            })

    def add_user(self, user_level=''):
        """
        Adds a new user
        
        Edit a specific users filtered with `/pk/`
        
        :param str user_level: the new user level
        :return: returns true if a new user is created
        :rtype: True or False
        """
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
