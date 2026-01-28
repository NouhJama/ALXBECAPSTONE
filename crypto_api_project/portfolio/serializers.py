from  rest_framework import serializers
from .models import  Portfolio, Asset, Transaction, UserProfile
# Import get_user_model to reference the custom user model
from django.contrib.auth import get_user_model
from portfolio.services.coingecko import get_coin_price
from decimal import Decimal


# User Serializer
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 
            'username',
            'email',
            'password',
        ]
    
    # Ensure email is unique
    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    # Create user with hashed password
    def create(self, validated_data):
        password = validated_data.pop('password')
        # object.create_user handles password hashing
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        phone_number = validated_data.get('phone_number')
        
        user.save()
        return user

# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'bio', 'profile_picture', 'preferred_currency']
        ordering = ['id']

    
# Portfolio Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'owner', 'name', 'created_at']
        read_only_fields = ['owner', 'created_at']
        ordering = ['-created_at', 'id']

# Asset Serializer
class AssetSerializer(serializers.ModelSerializer):
    unrealized_profit_loss = serializers.SerializerMethodField()
    current_value = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['id', 'portfolio', 'coin_id', 'quantity', 'average_buy_price', 'realized_profit_loss', 
                  'unrealized_profit_loss', 'current_value', 'created_at', 'update_at'] 
        read_only_fields = ['id', 'portfolio', 'created_at', 'realized_profit_loss', 'update_at']
        ordering = ['-update_at', 'id']

    # Calculate unrealized profit/loss and current value
    def get_current_value(self, obj):
        current_price = get_coin_price(obj.coin_id, currency="usd")
        if current_price is not None and current_price.get("success", True):
            # convert to Decimal for accurate calculations
            current_price = Decimal(str(current_price.get("price", 0.00)))
            return current_price * Decimal(str(obj.quantity))
        return 0.00
    
    def get_unrealized_profit_loss(self, obj):
        current_price = get_coin_price(obj.coin_id, currency="usd")
        if current_price is not None and current_price.get("success", True):
            # convert to Decimal for accurate calculations
            quantity = Decimal(str(obj.quantity))
            average_buy_price = Decimal(str(obj.average_buy_price))
            current_price = Decimal(str(current_price.get("price", 0.00)))
            return (current_price - average_buy_price) * quantity
        return 0.00

# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'asset', 'transaction_type', 'quantity', 'price_per_unit', 'total_value', 'transaction_date']
        read_only_fields = ['id', 'asset', 'price_per_unit', 'total_value', 'transaction_date']
        ordering = ['-transaction_date', 'id']