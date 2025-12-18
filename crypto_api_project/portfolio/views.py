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

