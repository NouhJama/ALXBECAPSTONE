from django.contrib import admin
from .models import CustomUser, UserProfile, Portfolio, Asset, Transaction

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'preferred_currency')
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    ordering = ('-created_at',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('coin_id', 'portfolio', 'quantity', 'average_buy_price', 'created_at', 'update_at')
    search_fields = ('coin_id', 'portfolio__name')
    ordering = ('-created_at', '-update_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'asset', 'quantity', 'price_per_unit', 'total_value', 'transaction_date')
    search_fields = ('transaction_type', 'asset__coin_id')
    ordering = ('-transaction_date',)   