from django.test import TestCase
from django.db import transaction
from django.db import Error
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from home.models import userModel


class AppUsersTests(TestCase):
    def setUp(self):
        g_admin = Group.objects.create(name="Administrators")
        g_publ = Group.objects.create(name="Publishers")
        g_auth = Group.objects.create(name="Authors")

    def test_users(self):
        """
        Create app user in Administrator group
        """
        try:
            admin = userModel.Admin.objects.create_user(
                username='admin',
                email='admin@email.com',
                password='adminpass',
                user_level= userModel.AppUser.ADMIN,
            )
        except Error as e:
            print('>Test Error: ', e)

    #def test_delete_app_user(self):
    #    """Delete AppUser objects """
    #    Author.objects.get(username='publisher').delete()
    #    Author.objects.get(username='publisher').delete()
    #    Author.objects.get(username='admin').delete()

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

