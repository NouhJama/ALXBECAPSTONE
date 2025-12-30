from decimal import Decimal
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from .serializers import (
    UserCreateSerializer, PortfolioSerializer, 
    AssetSerializer, TransactionSerializer, UserProfileSerializer 
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Portfolio, Asset, Transaction, UserProfile
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from portfolio.services.coingecko import get_coin_price
from django.db import transaction
from portfolio.pagination import TransactionCursorPagination, AssetCursorPagination

# Create your views here.
class UserCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit profiles to the authenticated user
        return self.queryset.filter(user=self.request.user)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Create or retrieve token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

# Portofolio, Asset, and Transaction views would go here
class PortfolioViewSet(viewsets.ModelViewSet):
    # Implementation for Portfolio CRUD operations
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Pagination is not necessary for portfolios



    def get_queryset(self):
        # Limit portfolios to those owned by the authenticated user
        portfolio_pk = self.kwargs.get('portfolio_pk')
        if portfolio_pk:
            # Nested routing case: return specific portfolio if it belongs to the user
            return self.queryset.filter(id=portfolio_pk, owner=self.request.user)
        # General case: return all portfolios owned by the user
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)

class AssetViewSet(viewsets.ModelViewSet):
    # Implementation for Asset CRUD operations
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = AssetCursorPagination

    def get_queryset(self):
        # Limit assets to those in portfolios owned by the authenticated user
        # Get the portfolio ID from the URL if nested routing is used
        portfolio_id = self.kwargs.get('portfolio_pk') # For nested routing
        if portfolio_id:
            return self.queryset.filter(portfolio__id=portfolio_id, portfolio__owner=self.request.user)
        # Otherwise, return all assets in portfolios owned by the user
        return self.queryset.filter(portfolio__owner=self.request.user)   
     
    # Automatically set the portfolio based on the request data
    def perform_create(self, serializer):
        portfolio_pk = self.kwargs.get('portfolio_pk')  
        if not Portfolio.objects.filter(id=portfolio_pk, owner=self.request.user).exists():
            raise PermissionDenied("You do not have permission to add assets to this portfolio.")
        
        portfolio_instance = Portfolio.objects.filter(id=portfolio_pk, owner=self.request.user).first()   
        serializer.save(portfolio=portfolio_instance)

    # Delete an asset and return custome message
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # Get the asset instance to be deleted
        symbol = instance.coin_id.upper() # Get the coin symbol for message
        self.perform_destroy(instance) # Delete the asset
        return Response({f"'detail': 'Asset {symbol} deleted successfully.'"},
                        status = status.HTTP_200_OK)
    
"""
- Transaction ViewSet with create, list, and retrieve functionalities.
- Delete functionality is immutable to preserve transaction history.
- Ensures transactions are linked to assets in portfolios owned by the authenticated user.
- Updates asset's average buy price and quantity on BUY transactions.
- Prevents selling more than owned on SELL transactions.
- Custom error handling for insufficient balance.
"""    
class TransactionViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    # Implementation for Transaction CRUD operations
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = TransactionCursorPagination

    def get_queryset(self):
        # Limit transactions to those for assets in portfolios owned by the authenticated user
        asset_id = self.kwargs.get('asset_pk') # For nested routing
        if asset_id:
            queryset = self.queryset.filter(asset__id=asset_id, asset__portfolio__owner=self.request.user)
            return queryset
        return self.queryset.filter(asset__portfolio__owner=self.request.user)    
    # Automatically set the asset based on the request data
    @transaction.atomic
    def perform_create(self, serializer):
        asset_id = self.kwargs.get('asset_pk')
        asset = Asset.objects.filter(id=asset_id, portfolio__owner=self.request.user).first()
        # Avoid processing if asset not found or access denied
        if not asset:
            raise ValidationError("Asset not found or access denied.")
        
        #Get the values from the validated data
        transaction_type = serializer.validated_data.get('transaction_type')
        quantity = serializer.validated_data.get('quantity')
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")    
        # Fetch live price for the asset
        price_response = get_coin_price(asset.coin_id, currency="usd")  
        # check if price fetch was successful
        if not price_response or not price_response.get("success", True):
            raise ValidationError("Could not fetch live price for the asset.")   
        price_per_unit = Decimal(str(price_response.get("price", 0.00)))
        
        # calculate total value
        total_value = price_per_unit * quantity
        
        if transaction_type == "BUY":
            # Calculate the new average buy price based on the existing quantity and price plus the new purchase
            total_cost = (asset.average_buy_price * asset.quantity) + (price_per_unit * quantity)
            total_quantity = asset.quantity + quantity

            # Avoid division by zero errorl
            if total_quantity > 0:
                asset.average_buy_price = total_cost / total_quantity
            asset.quantity = total_quantity
        elif transaction_type == "SELL":

            # check if user is trying to sell more than they own
            if quantity > asset.quantity:
                raise ValidationError("Insufficient balance.")
            
            # Calculate realized profit/loss for the sold quantity
            profit_loss = (price_per_unit - asset.average_buy_price) * quantity
            asset.realized_profit_loss += profit_loss
            
            # Sell transaction reduces the quantity
            asset.quantity -= quantity
        serializer.save(
            asset=asset,
            price_per_unit=price_per_unit,
            total_value=total_value

            )
        asset.save()

# Portfolio specific view to get list of transactions
class PortfolioTransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TransactionCursorPagination

    def get_queryset(self):
        portfolio_id = self.kwargs.get('portfolio_pk')
        return Transaction.objects.filter(
            asset__portfolio__id=portfolio_id,
            asset__portfolio__owner=self.request.user
        ).order_by('-transaction_date')
