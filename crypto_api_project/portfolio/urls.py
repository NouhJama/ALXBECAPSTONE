from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'portfolios', views.PortfolioViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Authentica endpoints
urlpatterns += [
    path('api/auth/register', views.RegisterView.as_view(), name='register'),
    path('api/auth/login', views.LoginView.as_view(), name='login'),
    path('api/auth/logout', views.LogoutView.as_view(), name='logout'),
    path('api/auth/user', views.UserDetailView.as_view(), name='user-profile'),
]

# Porto endpoints
urlpatterns += [
  path('portofolios/<int:portfolio_id>/summary/', views.PortfolioSummaryView.as_view(), name='portfolio-summary'),
 ]


