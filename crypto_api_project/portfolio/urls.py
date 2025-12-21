from django.urls import path, include
from .views import UserCreateView, LoginView, PortfolioViewSet, AssetViewSet, TransactionViewSet, UserProfileViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


router = DefaultRouter()
# You can register other viewsets here as needed
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')   
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile') 

# Nested router for assets under portfolios
portfolio_router = NestedDefaultRouter(router, r'portfolios', lookup='portfolio')   
portfolio_router.register(r'assets', AssetViewSet, basename='portfolio-assets') 

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    ]

urlpatterns += router.urls
urlpatterns += portfolio_router.urls
