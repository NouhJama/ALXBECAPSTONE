from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from portfolio.models import Asset, Portfolio
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Setup user+auth+portfolio for asset tests
class AssetAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a portfolio for the user
        self.portfolio = Portfolio.objects.create(
            owner=self.user,
            name="Test Portfolio"
        )

    def test_create_asset(self):
        url = reverse('portfolio-assets-list', kwargs={'portfolio_pk': self.portfolio.pk})
        data = {
            "coin_id": "bitcoin",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.count(), 1)
        self.assertEqual(Asset.objects.get().coin_id, "bitcoin")
        self.assertEqual(Asset.objects.get().portfolio, self.portfolio)