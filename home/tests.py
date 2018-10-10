from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser

from .models import Article, Topic


class AppUsersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.foo = Foo.objects.create(bar="Test")
        ...

    def test_created_user_authors_permissions(self):
        # The signed up users are in the authors goup

    def test_users_can_create_articles(self):
        # All users can create articles

    def test_editors_and_admin_can_publish(self):
        # Users with editors and admin group can publish articles

    def test_editors_cannot_publish_own_articles(self):
        # Editors cannot publish their own articles

    def test_anon_users_can_only_view(self):
        # Anonymous users can only view articles using GET

class ArticleModelTest(TestCase):
    def test_article_created_is_not_published(self):
        # A new article is not published

    def test_publish_date_is_not_future(self):
        # An article cannot be published in the future

    def test_published_article_cannot_be_deleted(self):
        # A published article cannot be deleted except by an admin

    def test_article_can_be_deleted_by_owner_or_editor_or_admin(self):
        # An article can only be deleted by the owner or editor or admin

class AppClientTestCase(TestCase):
    def test_client_Example(self):
        pass
