from  rest_framework import serializers
from .models import  Portfolio, Asset, Transaction
# Import get_user_model to reference the custom user model
from django.contrib.auth import get_user_model


# User Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 
            'username',
            'email',
            'phone_number',
            'bio',
            'profile_picture',
            'preferred_currency',
            'date_joined',
        ]

    # Ensure email is unique
    def validate_email(self, value):
        if get_user_model.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
# Portfolio Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'owner', 'name', 'created_at']
        read_only_fields = ['owner', 'created_at']

# Asset Serializer
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'portfolio', 'symbol', 'quantity', 'purchase_price', 'purchase_date']
        read_only_fields = ['portfolio']

# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'asset', 'transaction_type', 'quantity', 'price_per_unit', 'transaction_date']
        read_only_fields = ['asset']