from django.test import TestCase
from portfolio.models import CustomUser, UserProfile, Portfolio, Asset, Transaction

# Test cases for User creation and related models
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")

# UserProfile model tests
class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="profileuser",
            email="profileuser@example.com",
            password="profilepassword123"
        )