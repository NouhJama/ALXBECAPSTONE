from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from portfolio.models import Portfolio
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class PortfolioAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_portfolio(self):
        url = reverse('portfolio-list')
        data = {
            "name": "My Crypto Portfolio"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Portfolio.objects.count(), 1)
        self.assertEqual(Portfolio.objects.get().name, "My Crypto Portfolio")
        self.assertEqual(Portfolio.objects.get().owner, self.user)