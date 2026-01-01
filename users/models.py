from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('donor', 'Individual Donor'),
        ('business', 'Business Donor'),
        ('recipient', 'Recipient'),
        ('organization', 'Verified Organization'),
        ('moderator', 'Community Moderator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='donor')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
