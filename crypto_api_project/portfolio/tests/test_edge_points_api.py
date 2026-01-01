from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from portfolio.models import Asset, Portfolio, Transaction
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from decimal import Decimal

class TestAverageBuyPriceCalculation(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a portfolio for the user
        self.portfolio = Portfolio.objects.create(
            owner=self.user,
            name="Test Portfolio")
        
        # Create an asset in the portfolio
        self.asset = Asset.objects.create(
            portfolio=self.portfolio,
            coin_id="bitcoin",
            
        )

        self.url = reverse('asset-transactions-list', kwargs={
            'portfolio_pk': self.portfolio.pk,
            'asset_pk': self.asset.pk
        })

    def test_average_buy_price_and_quantity(self):
        # Create multiple BUY transactions
        response1 = self.client.post(self.url, {
            "transaction_type": "BUY",
            "quantity": Decimal("0.5")
        }, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(self.url, {
            "transaction_type": "BUY",
            "quantity": Decimal("1.0")
        }, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.asset.refresh_from_db()

        self.assertEqual(self.asset.quantity, Decimal("1.5"))
        expected_average_price = ((Decimal("0.5") * Decimal("30000.0")) + (Decimal("1.0") * Decimal("35000.0"))) / Decimal("1.5")

