from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Extend the default User model with a UserProfile
class UserProfile(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # Additional profile fields
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        username = getattr(self.user, 'username', None) or str(self.user)
        return f"Profile for {username}"

# Signal to create or update UserProfile whenever a User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
