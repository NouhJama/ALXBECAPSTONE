from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from portfolio.models import Asset, Portfolio, Transaction
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from decimal import Decimal

class TransactionAPITest(APITestCase):
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
        # Create an asset in the portfolio
        self.asset = Asset.objects.create(
            portfolio=self.portfolio,
            coin_id="bitcoin"
        )
    def test_create_transaction(self):
        url = reverse('asset-transactions-list', kwargs={
            'portfolio_pk': self.portfolio.pk,
            'asset_pk': self.asset.pk
        })
        data = {
            "transaction_type": "BUY",
            "quantity": Decimal("0.5"),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().transaction_type, "BUY")
        self.assertEqual(Transaction.objects.get().quantity, Decimal("0.5"))
        self.assertEqual(Transaction.objects.get().asset, self.asset)  

    # test list of transactions  
    def test_list_transactions(self):
        # Create a transaction first
        Transaction.objects.create(
            asset=self.asset,
            transaction_type="BUY",
            quantity=Decimal("0.5"),
            price_per_unit=Decimal("30000.0"),
            total_value=Decimal("15000.0")
        )
        url = reverse('asset-transactions-list', kwargs={
            'portfolio_pk': self.portfolio.pk,
            'asset_pk': self.asset.pk
        })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['transaction_type'], "BUY")
        self.assertEqual(float(response.data['results'][0]['quantity']), 0.5)
        self.assertEqual(float(response.data['results'][0]['price_per_unit']), 30000.0)
        self.assertEqual(float(response.data['results'][0]['total_value']), 15000.0)