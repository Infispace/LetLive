"""
:synopsis: Used to test `home.models.userModel` models
"""
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django_seed import Seed
from home.models import Admin
from .testUtils import TestUtils


class UserClientTests(TestCase, TestUtils):
    """
    Test the home.models.userModel.AppUser Model
    """
    client = Client()     #: django test client
    
    def setUp(self):
        # seed test user
        username = self.create_username()
        self.user = User.objects.create(username=username)

    def test_redirect_login(self):
        """
        Test redirect before login for `home:user_profile` url.
        Should redirect to `home:user_login` url.
        """
        response = self.client.get(reverse('home:user_profile'))
        
        # the expected redirect url
        redirect_url = (
            reverse('home:user_login')
            + '?next=' 
            + reverse('home:user_profile')
        )

        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_url)

    def test_user_403(self):
        """
        Test permission for `home:user_new` and `home:user_default` url.
        Only users with admin privilages can access this page.
        Should respond with status code 403.
        """
        # client login
        self.client.force_login(user=self.user)

        # request
        response_new = self.client.get(reverse('home:user_new'))
        response_default = self.client.get(reverse('home:user_default'))

        # assert response
        self.assertEqual(response_new.status_code, 403)
        self.assertEqual(response_default.status_code, 403)

        # client logout
        self.client.logout()

    def test_edit_user_profile(self):
        """
        Test edit user profile for `home:user_profile_edit` url.
        Redirects to `home:user_profile` url if success.
        """
        # client login
        self.client.force_login(user=self.user)
        
        # request
        email = self.seeder.faker.safe_email()
        response = self.client.post(reverse('home:user_profile_edit'), {
            'email': email,
        })

        # get changed user
        self.user = User.objects.get(username=self.user.username)

        # assert response
        self.assertEqual(email, self.user.email)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:user_profile'))
     
        # client logout
        self.client.logout()
        
    def test_change_user_password(self):
        """
        Test change user password for `home:password_change` url.
        Redirects to `home:password_change_done` url if success.
        """
        # old passwod details
        old_password = self.seeder.faker.word()
        self.user.set_password(old_password)
        self.user.save()

        # client login
        login = self.client.force_login(user=self.user)

        # new password details
        new_password = self.create_password()

        # request
        response = self.client.post(reverse('home:password_change'), {
            'old_password': old_password,
            'new_password1': new_password,
            'new_password2': new_password,
        })

        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:password_change_done'))

        # client logout
        self.client.logout()

    def test_new_user(self):
        """
        Test create new user for `home:user_new` url.
        """
        # client login with Admin user
        admin = Admin.objects.create(user=self.user)
        self.client.force_login(user=self.user)
        
        # user details
        username = self.create_username()
        password = self.create_password()
        
        # request
        response = self.client.post(reverse('home:user_new'), {
            'email': self.seeder.faker.safe_email(),
            'username': username,
            'password1': password,
            'password2': password,
            'is_author': False,
        })

        # assert response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home:user_default'))

        # client logout
        self.client.logout()

    def test_list_users(self):
        """
        Test list user for `home:user_default` url.
        """
        # client login with Admin user
        admin = Admin.objects.create(user=self.user)
        self.client.force_login(user=self.user)

        response = self.client.get(reverse('home:user_default'))
        
        # assert response
        self.assertIsInstance(response.context['authors_list'], QuerySet)
        self.assertIsInstance(response.context['publishers_list'], QuerySet)

        # client logout
        self.client.logout()

