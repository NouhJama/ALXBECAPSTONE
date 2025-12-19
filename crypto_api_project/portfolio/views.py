from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer, PortfolioSerializer, AssetSerializer, TransactionSerializer 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Portfolio, Asset, Transaction

# Create your views here.
class UserCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

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
class PortfolioViewSet(ModelViewSet):
    # Implementation for Portfolio CRUD operations
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit portfolios to those owned by the authenticated user
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)

class AssetViewSet(ModelViewSet):
    # Implementation for Asset CRUD operations
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit assets to those in portfolios owned by the authenticated user
        return self.queryset.filter(portfolio__owner=self.request.user)
    
    # Automatically set the portfolio based on the request data
    def perform_create(self, serializer):
        serializer.save()

class TransactionViewSet(ModelViewSet):
    # Implementation for Transaction CRUD operations
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit transactions to those for assets in portfolios owned by the authenticated user
        return self.queryset.filter(asset__portfolio__owner=self.request.user)
    
    # Automatically set the asset based on the request data
    def perform_create(self, serializer):
        transaction = serializer.save()
        asset = transaction.asset
        # Update asset's average buy price and quantity if it's a BUY transaction
        if transaction.transaction_type == "BUY":
            # Calculate the new average buy price based on the existing quantity and price plus the new purchase
            total_cost = (asset.average_buy_price * asset.quantity) + (transaction.price_per_unit * transaction.quantity)
            total_quantity = asset.quantity + transaction.quantity
            asset.average_buy_price = total_cost / total_quantity
            asset.quantity = total_quantity
        elif transaction.transaction_type == "SELL":
            # Sell transaction reduces the quantity
            asset.quantity -= transaction.quantity
        asset.save()
