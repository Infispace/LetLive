"""
:synopsis: Used to test api_v1 authentication.
"""
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api_v1.views import ArticleViewSet
from home.models import userModel
from home.tests.testUtils import TestUtils

class AuthTests(APITestCase, TestUtils):
    """
    Test the authentication views for 
    registering users ,login and logout.
    """
    #: Using the standard RequestFactory API to create a form POST request.
    factory = APIRequestFactory()
    client = APIClient()
    
    username = None     #: username of test user
    password = None     #: password of test user

    def setUp(self):
        # test user attributes
        self.username = self.create_username()
        self.password = self.create_password()
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        
    def test_login_required(self):
        """
        Test Api is only available to authenticated users.
        """
        response = self.client.get('/api_v1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_articles_public(self):
        """
        Test `/api_v1/articles/` get endpoint is available to anonymous users.
        """
        request = self.factory.get('/api_v1/articles/')
        view = ArticleViewSet.as_view({'get': 'list'})
        
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_registration(self):
        pass

    def test_basic_login(self):
        pass
        
    def test_token_login(self):
        pass
        
    def test_logout(self):
        pass

