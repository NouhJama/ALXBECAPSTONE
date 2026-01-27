from django.urls import path, include
from .views import (
    UserCreateView, 
    PortfolioViewSet, 
    AssetViewSet, TransactionViewSet, 
    UserProfileViewSet, 
    PortfolioTransactionsViewSet,
    LogoutView
)
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from drf_spectacular.views import(
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)


router = DefaultRouter()
# You can register other viewsets here as needed
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')   
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile') 

# Nested router for assets under portfolios
asset_router = NestedDefaultRouter(router, r'portfolios', lookup='portfolio')   
asset_router.register(r'assets', AssetViewSet, basename='portfolio-assets') 

# Nested router for the transactions under assets (if needed)
transaction_router = NestedDefaultRouter(asset_router, r'assets', lookup='asset')
transaction_router.register(r'transactions', TransactionViewSet, basename='asset-transactions') 

# Nested router for all transactions under portfolios
portfolio_transactions_router = NestedDefaultRouter(router, r'portfolios', lookup='portfolio')
portfolio_transactions_router.register(r'transactions', PortfolioTransactionsViewSet, basename='portfolio-transactions')

urlpatterns = [
    # User registration and authentication routes
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("logout/", LogoutView.as_view(), name="user-logout"),

    # API schema and documentation routes
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += router.urls
urlpatterns += asset_router.urls
urlpatterns += transaction_router.urls
urlpatterns += portfolio_transactions_router.urls  