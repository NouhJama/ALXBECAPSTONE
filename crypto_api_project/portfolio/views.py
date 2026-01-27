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
from rest_framework.response import Response
from .models import Portfolio, Asset, Transaction, UserProfile
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from portfolio.services.coingecko import get_coin_price
from portfolio.services.request_meta import get_client_ip
from django.db import transaction
from portfolio.pagination import TransactionCursorPagination, AssetCursorPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .throttles import LoginRateThrottle
from rest_framework.views import APIView
from .permissions import (
    IsOwner,
    IsAssetOwner,
    IsTransactionOwner
)
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)


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
    
# Login view with JWT token generation
class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]

# Logout view to blacklist the refresh token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token to log them out
        try:
            # Get/extract the token from the request header
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({'detail': 'Refresh token is required.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)# Store the token
            token.blacklist()  # Blacklist the refresh token
            return Response({'detail': 'Successfully logged out.'}, 
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Error during logout.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
         

# Portofolio, Asset, and Transaction views would go here
class PortfolioViewSet(viewsets.ModelViewSet):
    # Implementation for Portfolio CRUD operations
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    permission_classes = [IsAuthenticated, IsOwner] # Only authenticated users can access
    pagination_class = None  # Pagination is not necessary for portfolios



    def get_queryset(self):
        # Limit portfolios to those owned by the authenticated user
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)
        client_ip = get_client_ip(self.request)
        logger.info(
            "PORTFOLIO_CREATED - User: %s, Portfolio ID: %s, IP: %s",
            self.request.user.username,
            serializer.instance.id,
            client_ip
        )

class AssetViewSet(viewsets.ModelViewSet):
    # Implementation for Asset CRUD operations
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated, IsAssetOwner] # Only authenticated users can access
    pagination_class = AssetCursorPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(portfolio__owner=self.request.user)
        # Limit assets to those in portfolios owned by the authenticated user
        # Get the portfolio ID from the URL if nested routing is used
        portfolio_id = self.kwargs.get('portfolio_pk') # For nested routing
        if portfolio_id:
            queryset = queryset.filter(portfolio__id=portfolio_id)
        # Otherwise, return all assets in portfolios owned by the user
        return queryset   
     
    # Automatically set the portfolio based on the request data
    def perform_create(self, serializer):
        portfolio_pk = self.kwargs.get('portfolio_pk')
        # Guard againt missing portfolio_pk
        if not portfolio_pk:
            raise ValidationError("Portfolio ID is required to add an asset.")  
        # Ensure the portfolio belongs to the authenticated user    
        try:
            portfolio_instance = Portfolio.objects.get(id=portfolio_pk, owner=self.request.user) 
        except Portfolio.DoesNotExist:
            raise PermissionDenied("You do not have permission to add assets to this portfolio.")
        serializer.save(portfolio=portfolio_instance)
        logger.info(
            "ASSET_CREATED - User: %s, Asset ID: %s, Portfolio ID: %s",
            self.request.user.username,
            serializer.instance.id,
            portfolio_pk
        )

    # Delete an asset and return custome message
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # Get the asset instance to be deleted
        symbol = instance.coin_id.upper() # Get the coin symbol for message
        self.perform_destroy(instance) # Delete the asset
        client_ip = get_client_ip(request)
        logger.info(
            "ASSET_DELETED - User: %s, Asset ID: %s, IP: %s",
            request.user.username,
            instance.id,
            client_ip
        )
        return Response({"detail": f"Asset {symbol} deleted successfully."},
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
    permission_classes = [IsAuthenticated, IsTransactionOwner] # Only authenticated users can access
    pagination_class = TransactionCursorPagination

    def get_queryset(self):
        # Limit transactions to those for assets in portfolios owned by the authenticated user
        asset_id = self.kwargs.get('asset_pk') # For nested routing
        if not asset_id:
            return super().get_queryset().none()
        return super().get_queryset().filter(
            asset_id=asset_id,
            asset__portfolio__owner=self.request.user
        ).order_by('-transaction_date')
    # Automatically set the asset based on the request data
    @transaction.atomic
    def perform_create(self, serializer):
        asset_id = self.kwargs.get('asset_pk')
        # Guard against missing asset_id
        if not asset_id:
            raise ValidationError("Asset ID is required to add a transaction.") 
        # Ensure the asset belongs to a portfolio owned by the authenticated user
        try:
            asset = Asset.objects.select_for_update().get(
                id=asset_id, portfolio__owner=self.request.user)
        except Asset.DoesNotExist:
            raise PermissionDenied("Asset not found or access denied.")
        
        #Get the values from the validated data
        transaction_type = serializer.validated_data.get('transaction_type')
        quantity = serializer.validated_data.get('quantity')
        # Validate quantity(Avoid zero, negative, none)
        if not quantity or quantity <= 0:
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

            # Avoid division by zero error
            if total_quantity > 0:
                asset.average_buy_price = total_cost / total_quantity
            asset.quantity = total_quantity
        elif transaction_type == "SELL":

            # check if user is trying to sell more than they own
            if quantity > asset.quantity:
                client_ip = get_client_ip(self.request)
                logger.info(
                    "TRANSACTION_FAILED - User: %s, Asset ID: %s, Attempted Sell Quantity: %s, IP: %s",
                    self.request.user.username,
                    asset.id,
                    quantity,
                    client_ip
                )
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
        client_ip = get_client_ip(self.request)
        logger.info(
            "TRANSACTION_CREATED - User: %s, Transaction ID: %s, Asset ID: %s, Type: %s, IP: %s",
            self.request.user.username,
            serializer.instance.id,
            asset.id,
            transaction_type,
            client_ip
        )

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
