"""
:synopsis: Used to test `home.models.userModel` models
"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.test import TestCase
from django.db import Error
from django_seed import Seed
from home.models import userModel
from .testUtils import TestUtils


class AppUsersTests(TestCase, TestUtils):
    """
    Test the home.models.userModel.AppUser Model
    """
    
    def setUp(self):
        # seed test user
        username = self.create_username()
        self.user = User.objects.create(username = username)

    def test_create_user_admin(self):
        """
        Tests home.userModel.Admin.objects.create
        """
        try:
            # create AppUser of Admin model
            admin = userModel.Admin.objects.create(user=self.user)
            
            # assert user attribute
            self.assertEqual(admin.user_level, userModel.AppUser.ADMIN)

        except Error as e:
            print('>Test Error: ', e)

    def test_create_user_author(self):
        """
        Tests home.userModel.Author.objects.create
        """
        try:
            # create AppUser of Author model
            author = userModel.Author.objects.create(user=self.user)
            
            # assert user attribute
            self.assertEqual(author.user_level, userModel.AppUser.AUTHOR)

        except Error as e:
            print('>Test Error: ', e)

    def test_create_user_subscriber(self):
        """
        Tests home.userModel.AppUser.objects.create
        """
        try:
            # create AppUser of Subscriber model
            subscriber = userModel.Subscriber.objects.create(user=self.user)
            
            # assert user attribute
            self.assertEqual(subscriber.user_level, userModel.AppUser.SUBSCRIBER)

        except Error as e:
            print('>Test Error: ', e)

    def test_delete_app_user(self):
        """
        Delete home.userModel.AppUser objects 
        """
        # create AppUser of Author model
        author = userModel.Author.objects.create(user=self.user)
        
        # delete AppUser
        author.delete()
        
        # predict ObjectDoesNotExist thrown
        exception = None
        try:
            userModel.Admin.objects.get(user=author.user)
        except ObjectDoesNotExist as e:
            exception = e
        
        # assert ObjectDoesNotExist
        self.assertIsInstance(exception, ObjectDoesNotExist)

