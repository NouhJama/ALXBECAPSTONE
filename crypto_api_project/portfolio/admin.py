from django.contrib import admin
from .models import CustomUser, Portfolio, Asset, Transaction

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'preferred_currency', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    ordering = ('-created_at',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'portfolio', 'quantity', 'average_buy_price', 'purchase_date')
    search_fields = ('symbol', 'portfolio__name')
    ordering = ('-purchase_date',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'asset', 'quantity', 'price_per_unit', 'transaction_date')
    search_fields = ('transaction_type', 'asset__symbol')
    ordering = ('-transaction_date',)   