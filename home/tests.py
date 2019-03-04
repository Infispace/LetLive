from django.test import TestCase
from django.db import IntegrityError, transaction, Error
from django.contrib.auth.models import User, AnonymousUser, Group, Permission

from .models.userModel import AppUser, Author, Publisher, Admin

class AppUsersTests(TestCase):
    def setUp(self):
        g_admin = Group.objects.create(name="Administrators")
        g_publ = Group.objects.create(name="Publishers")
        g_auth = Group.objects.create(name="Authors")

    def test_create_admin(self):
        """
        Create app user in Administrator group
        """
        try:
            with transaction.atomic():
                admin = Admin.objects.create_user(
                    username='admin',
                    email='admin@email.com',
                    password='adminpass',
                    user_level= AppUser.ADMIN,
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

#class ArticleModelTest(TestCase):
    #def test_article_created_is_not_published(self):
        # A new article is not published

    #def test_future_published_article_not_shown(self):
        # An article can be published in the future
        # but should not be shown till published date

    #def test_published_article_cannot_be_deleted(self):
        # A published article cannot be deleted except by an admin

    #def test_article_can_be_deleted_by_owner_or_editor_or_admin(self):
        # An article can only be deleted by the owner or editor or admin

#class AppClientTestCase(TestCase):
    #def test_client_Example(self):
        #pass
