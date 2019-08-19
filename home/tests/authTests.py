"""
:synopsis: Used to test authentication views.
"""
from django.test import TestCase
from django.db import transaction
from django.db import Error
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from django_seed import Seed
from home.models import userModel


class AuthTests(TestCase):
    """
    Test the home.views.authView.*
    """
    seeder = None       #: django-seed instance
    client = None       #: django test clinet
    username = None     #: username of test user
    password = None     #: password of test user

    def setUp(self):
        self.seeder = Seed.seeder()
        self.client = Client()
        
        # test user attributes
        self.username = self.seeder.faker.first_name()
        self.password = self.seeder.faker.word()
        
        # create AppUser of Subscriber model
        userModel.Subscriber.objects.create_user(
            username=self.username,
            email=self.seeder.faker.email(),
            password=self.password,
            user_level= userModel.AppUser.SUBSCRIBER,
        )
        
    def test_sign_up_get(self):
        """
        user_register url GET.
        """    
        response = self.client.get(reverse('home:user_register'))
        response.content
        
        # assert response
        self.assertEqual(response.status_code, 200)
        
    def test_login_get(self):
        """
        user_login url GET.
        """    
        response = self.client.get(reverse('home:user_login'))
        response.content
        
        # assert response
        self.assertEqual(response.status_code, 200)
        
    def test_sign_up_post(self):
        """
        user_register url POST.
        Creates new users.
        """
        # test user password
        password = ''
        while (len(password) < 8):
            password += self.seeder.faker.word()

        # request
        response = self.client.post(reverse('home:user_register'), {
            'email': self.seeder.faker.safe_email(),
            'username': self.seeder.faker.first_name(),
            'password': password,
            'password2': password,
            'is_author': False,
        })
        
        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:index'))
        
        # get created user
        user = User.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)
        
        # client logout
        self.client.logout();
        
    def test_login_post(self):
        """
        user_login url POST.
        Authenticates an existing user.
        """
        # request
        response = self.client.post(reverse('home:user_login'), {
            'username': self.username,
            'password': self.password,
        })
        
        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:index'))
        
        # client logout
        self.client.logout();
        
    def test_logout(self):
        """
        user_login url POST.
        Authenticates an existing user.
        """
        # client login
        self.client.login(
            username=self.username, 
            password=self.password
        )
        
        # request
        response = self.client.get(reverse('home:user_logout'))
        
        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:index'))

