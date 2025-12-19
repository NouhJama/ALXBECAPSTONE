from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # Only create profile when a new user is created for the first time.
    if created:
        # Create an associated UserProfile for the new user.
        UserProfile.objects.create(user=instance) 
