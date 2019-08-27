"""
:synopsis: Used to test api_v1 authentication.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api_v1.views import ArticleViewSet

class AuthTests(APITestCase):
    """
    Test the authentication views for 
    registering users ,login and logout.
    """
    #: Using the standard RequestFactory API to create a form POST request.
    factory = APIRequestFactory()
    client = APIClient()

    def setUp(self):
        pass
        
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

