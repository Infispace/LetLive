"""
:synopsis: Used to test user permissions.
"""
from django.test import TestCase
from django.db import transaction
from django.db import Error
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from home.models import userModel
from django_seed import Seed


class UserPermissionTests(TestCase):
    """
    Test the `django.contrib.auth.models.Permission`
    """
    #: django-seed instance
    seeder = None
    
    def setUp(self):
        self.seeder = Seed.seeder()

    #def test_created_user_authors_permissions(self):
        # The signed up users are in the authors goup

    #def test_users_can_create_articles(self):
        # All users can create articles

    #def test_editors_and_admin_can_publish(self):
        # Users with editors and admin group can publish articles

    #def test_editors_cannot_publish_own_articles(self):
        # Editors cannot publish their own articles

    #def test_anon_users_can_only_view(self):
        # Anonymous users can only view articles using GET

