"""
:synopsis: Used to define the views to manage users
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from home.forms import RegisterUserForm
from home.forms import DeleteUserForm
from home.models import Admin
from home.models import Author
from home.models import Subscriber

class UsersView(PermissionRequiredMixin, TemplateView):
    """
    Class to manage users. Add and delete users. 
    Admins only can access this view.
    """
    #: The permissions required to access the view.
    permission_required = (
        'auth.add_user',
        'auth.delete_user',
    )
    #: The html template to render.
    template_name = 'home/user_templates/users_base.html'
    #: The list of users with admin user level.
    admins_list = None
    #: The list of users with author user level.
    authors_list = None
    #: The list of users with subscribers user level.
    subscribers_list = None
    #: The form to render.
    user_form = None
    #: The error to be displayed.
    error_string = ''
    #: The user to view or edit.
    view_user = None

    def get_permission_required(self):
        permission_required = super().get_permission_required()
        page = self.get_context_data()['page']
        
        # permission against http method post
        # restrict to new and delete
        permited = False;
        if page == 'user_new' or page == 'user_delete':
            permited = True;

        if self.request.method == 'POST' and not permited:
            raise PermissionDenied

        return permission_required

    def get(self, request, user_id=0, *args, **kwargs):
        """
        Display users list with filters `/authors/` and `/subcribers/`.
        
        Shows A specific users filtered with `/pk/`.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param int user_id: the user id to filter
        """
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # get user list
        if page == 'user_admin':
            self.admins_list = Admin.objects.all()
        elif page == 'user_author':
            self.authors_list = Author.objects.all()
        elif page == 'user_subscriber':
            self.subscribers_list = Subscriber.objects.all()
        
        # get  user with pk
        if user_id != 0:
            self.view_user = get_object_or_404(User, pk=user_id)
            
        # set form to render
        if page == 'user_delete':
            self.user_form = DeleteUserForm(instance=self.view_user)
        elif page == 'user_new':
            self.user_form = RegisterUserForm()

        # render template
        if page == 'user_view':
            self.template_name = 'home/account.html'

        return self.render_to_response({
            'page': page,
            'admins_list': self.admins_list,
            'authors_list': self.authors_list,
            'subscribers_list': self.subscribers_list,
            'user_form': self.user_form,
            'view_user': self.view_user,
        })

    def post(self, request, user_id=0, *args, **kwargs):
        """
        Creates a new user `/new/`.
        
        Edit a specific users filtered with `/pk/`
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param int user_id: the user id to filter
        """
        # get page context
        context = self.get_context_data()
        page = context['page']

        # get user from user_id
        if user_id != 0:
            self.view_user = get_object_or_404(User, pk=user_id)
        
        # get form to validate
        if page == 'user_new':
            self.user_form = RegisterUserForm(request.POST)
        elif page == 'user_delete':
            self.user_form = DeleteUserForm(
                request.POST, 
                instance=self.view_user
            )
        
        # make db edits
        try:
            success = self.user_form.is_valid()
            if success and page == 'user_delete':
                self.view_user.delete()
            elif success and page == 'user_new':
                user = self.user_form.save()

            success = True
        except Exception as e:
            success = False
            self.error_string = 'There was an error. Please try again.' 
            if settings.DEBUG:
                self.error_string = e
        
        # render template
        if success:
            return HttpResponseRedirect(reverse('home:user_default'))
        else:
            return self.render_to_response({
                'page': page,
                'view_user': self.view_user,
                'user_form': self.user_form,
                'error_string': self.error_string,
            }, status=400)

