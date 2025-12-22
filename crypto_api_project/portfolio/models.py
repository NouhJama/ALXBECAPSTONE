from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username
    
# Profile Model
class UserProfile(models.Model):   
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)   
    preferred_currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return f"Profile of {self.user.username}"


#Portofolio, Asset and Transaction models
class Portfolio(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Asset(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="assets"
    )
    symbol = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, default=0.00)
    average_buy_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.symbol} in {self.portfolio.name}"
    
class Transaction(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=10, choices=[("BUY", "Buy"), ("SELL", "Sell")])
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} of {self.asset.symbol} at {self.price_per_unit} on {self.transaction_date}"
    
