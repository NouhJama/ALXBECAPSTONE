from django.urls import path, include
from .views import UserCreateView, LoginView, PortfolioViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# You can register other viewsets here as needed
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    ]

urlpatterns += router.urls
