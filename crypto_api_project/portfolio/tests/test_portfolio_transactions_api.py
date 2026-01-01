from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from portfolio.models import Asset, Portfolio, Transaction
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from decimal import Decimal

class PortfolioTransactionAPITest(APITestCase):
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

        # Create an asset in the portfolio(Bitcoin)
        self.btc_asset = Asset.objects.create(
            portfolio=self.portfolio,
            coin_id="bitcoin"
        )

        # Create an asset in the portfolio(Ethereum)
        self.eth_asset = Asset.objects.create(
            portfolio=self.portfolio,
            coin_id="ethereum"
        )
        # Create a transaction for Bitcoin asset
        self.transaction = Transaction.objects.create(
            asset=self.btc_asset,
            transaction_type="BUY",
            quantity=Decimal("0.5"),
            price_per_unit=Decimal("30000.0"),
            total_value=Decimal("15000.0")
        )

        # Create a transaction for Ethereum asset
        self.eth_transaction = Transaction.objects.create(
            asset=self.eth_asset,
            transaction_type="BUY",
            quantity=Decimal("2.0"),
            price_per_unit=Decimal("2000.0"),
            total_value=Decimal("4000.0")
        )  

    def test_list_transactions_for_portfolio(self):

        # Build the url with portfolio id only to list transactions
        url = reverse('portfolio-transactions-list', kwargs={
            'portfolio_pk': self.portfolio.id,
        })

        response = self.client.get(url)

        # Assert the response status code and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Two transactions created in setUp

"""
-- New Test Case for Empty Portfolio Transactions
--- This test case checks the behavior of listing transactions
--- for a portfolio that has no transactions, but does have assets.
"""
class TestEmptyPortfolioTransactions(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="emptyuser",
            email="emptyuser@example.com",
            password="emptypassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a portfolio for the user
        self.portfolio = Portfolio.objects.create(
            # Make sure to use the correct owner field
            owner=self.user,
            name="Empty Portfolio"
        )

        # Create an asset in the portfolio (no transactions)
        self.asset = Asset.objects.create(
            portfolio=self.portfolio,
            coin_id="litecoin"
        )

        self.asset2 = Asset.objects.create(
            portfolio=self.portfolio,
            coin_id="ripple"
        )


    def test_list_transactions_empty_portfolio(self):

        # Build the url with portfolio id only to list transactions
        url = reverse('portfolio-transactions-list', kwargs={
            'portfolio_pk': self.portfolio.id,
        })

        response = self.client.get(url)

        # Assert the response status code and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # No transactions in this portfolio