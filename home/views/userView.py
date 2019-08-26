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
from home.models import Publisher
from home.models import Author

class UsersView(PermissionRequiredMixin, TemplateView):
    """
    Class to manage users. Add and delete users. 
    Admins only can access this view.
    """
    #: The permissions required to access the view.
    permission_required = (
        'home.add_publisher',
        'home.delete_publisher',
        'home.delete_author'
    )
    #: The html template to render.
    template_name = 'home/users.html'
    #: The list of users with author user level.
    authors_list = None
    #: The list of users with publisher user level.
    publisers_list = None
    #: The form to render.
    user_form = None
    #: The error to be displayed.
    error_string = ''
    #: The user to view or edit.
    view_user = None

    @transaction.atomic
    def add_publisher(self):
        """
        Adds a new user of publisher user_level
        
        Edit a specific users filtered with `/pk/`
        
        :return: returns true if a new user is created
        :rtype: True or False
        """
        success = False
        # create new user
        user = self.user_form.save()
        success = Publisher.objects.create(user=user)
        
        return success

    def get(self, request, user_id=0, *args, **kwargs):
        """
        Display users list with filters `/authors/` and `/publishers/`.
        
        Shows A specific users filtered with `/pk/`.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param int user_id: the user id to filter
        """
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # get user list or user with pk
        if user_id == 0:
            self.authors_list = Author.objects.all()
            self.publisers_list = Publisher.objects.all()
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
            
        return self.render_to_response({
            'page': page,
            'authors_list': self.authors_list,
            'publishers_list': self.publisers_list,
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
                request.POST, 
                instance=self.view_user
            )
        
        # make db edits
        try:
            success = self.user_form.is_valid()
            if success and page == 'user_delete':
                self.view_user.delete()
                success = True
            elif success and page == 'user_new':
                success = self.add_publisher()
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

