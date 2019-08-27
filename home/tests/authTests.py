"""
:synopsis: Used to test authentication views.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.test import TestCase
from django.db import transaction
from django.db import Error
from django.urls import reverse
from django.test import Client
from django_seed import Seed
from home.models import userModel
from .testUtils import TestUtils


class AuthTests(TestCase, TestUtils):
    """
    Test the authentication views for 
    registering users ,login and logout.
    """
    client = Client()   #: django test client
    username = None     #: username of test user
    password = None     #: password of test user

    def setUp(self):
        # test user attributes
        self.username = self.create_username()
        self.password = self.create_password()
        user = User.objects.create(username=self.username)
        user.set_password(self.password)

        # create AppUser of Admin model
        admin = userModel.Admin.objects.create(user=user)
        
    def test_sign_up_get(self):
        """
        `home:user_register` url GET.
        Should return status code 200.
        """    
        response = self.client.get(reverse('home:user_register'))
        
        # assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'signup')
        
    def test_login_get(self):
        """
        `home:user_login` url GET.
        Should return status code 200.
        """    
        response = self.client.get(reverse('home:user_login'))
        
        # assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'login')
        
    def test_sign_up_post(self):
        """
        `home:user_register` url POST. Creates new users if successful.
        Should return status code 302 and redirect to `home:user_login` url.
        """
        # user details
        username = self.create_username()
        password = self.create_password()

        # request
        response = self.client.post(reverse('home:user_register'), {
            'email': self.seeder.faker.safe_email(),
            'username': username,
            'password1': password,
            'password2': password,
            'is_author': False,
        })

        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:user_login'))
        
        # get created user
        user = User.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)
        
        # client logout
        self.client.logout();
        
    def test_login_post(self):
        """
        `home:user_login` url POST.
        Authenticates an existing user if successful.
        Should return status code 302 and redirect to `home:index` url.
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
        `home:user_logout` url POST.
        Logs out an authenticates an existing user if successful.
        Should return status code 302 and redirect to `home:index` url.
        """
        # client login
        self.client.login(username=self.username, password=self.password)
        
        # request
        response = self.client.get(reverse('home:user_logout'))

        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:index'))

