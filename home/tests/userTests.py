"""
:synopsis: Used to test `home.models.userModel` models
"""
from django.test import TestCase
from django.db import transaction
from django.db import Error
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from home.models import userModel
from django_seed import Seed


class AppUsersTests(TestCase):
    """
    Test the home.models.userModel.AppUser Model
    """
    #: django-seed instance
    seeder = None
    
    def setUp(self):
        self.seeder = Seed.seeder()

    def test_create_user(self):
        """
        Tests home.userModel.AppUser.objects.create_user
        """
        try:
            # user attributes
            username = self.seeder.faker.first_name()
            email = self.seeder.faker.email()
            
            # create AppUser of Admin model
            admin = userModel.Admin.objects.create_user(
                username=username,
                email=email,
                password=self.seeder.faker.word(),
                user_level= userModel.AppUser.ADMIN,
            )
            
            # assert user attribute
            self.assertEqual(admin.user.username, username)
            self.assertEqual(admin.user.email, email)

        except Error as e:
            print('>Test Error: ', e)

    def test_delete_app_user(self):
        """
        Delete home.userModel.AppUser objects 
        """
        # seed user
        self.seeder.add_entity(User, 1)
        inserted_pks = self.seeder.execute()
        
        # seed AppUser of Author model
        user = User.objects.get(pk=inserted_pks[User][0])
        self.seeder.add_entity(userModel.Author, 1, {
          'user': user
        })
        inserted_pks = self.seeder.execute()
        
        # delete AppUser
        author = userModel.Author.objects.get(user=user)
        author.delete()
        
        # predict ObjectDoesNotExist thrown
        exception = None
        try:
            userModel.Admin.objects.get(user=author.user)
        except ObjectDoesNotExist as e:
            exception = e
        
        # assert ObjectDoesNotExist
        self.assertIsInstance(exception, ObjectDoesNotExist)

