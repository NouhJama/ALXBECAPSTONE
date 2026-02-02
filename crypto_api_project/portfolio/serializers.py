from  rest_framework import serializers
from .models import  Portfolio, Asset, Transaction, UserProfile
# Import get_user_model to reference the custom user model
from django.contrib.auth import get_user_model
from portfolio.services.coingecko import get_coin_price
from decimal import Decimal
from PIL import Image # For image validation

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

    """ 
    -Validate profile picture size and type if needed.
    -Allow only extentions like .jpg, .png, .webp and limit size to 2MB.
    """
    def validate_profile_picture(self, value):
        max_size = 2 * 1024 * 1024  # 2MB
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
        min_dimension = 200  # Minimum width and height in pixels
        max_dimension = 2000  # Maximum width and height in pixels


        if value.size > max_size:
            raise serializers.ValidationError("Profile picture size should not exceed 2MB.")
        
        extension = value.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension. Allowed extensions: jpg, jpeg, png, webp.")

        # Validate image dimensions
        try:
            image = Image.open(value)
            width, height = image.size
            if width < min_dimension or height < min_dimension:
                raise serializers.ValidationError(f"Image dimensions should be at least {min_dimension}px by {min_dimension}px.")
            if width > max_dimension or height > max_dimension:
                raise serializers.ValidationError(f"Image dimensions should not exceed {max_dimension}px by {max_dimension}px.")
        except Exception as e:
            raise serializers.ValidationError("Invalid image file.")
        
        return value

    
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
        read_only_fields = ['id', 'portfolio', 'created_at', 'quantity', 'average_buy_price', 'realized_profit_loss', 'update_at', 'unrealized_profit_loss',]
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