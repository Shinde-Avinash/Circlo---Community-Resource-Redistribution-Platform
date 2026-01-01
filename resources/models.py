from django.db import models
from django.conf import settings
from django.utils import timezone

class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('books', 'Books'),
        ('supplies', 'Supplies'),
        ('other', 'Other'),
    )
    URGENCY_CHOICES = (
        ('red', '🔴 Immediate (Hours)'),
        ('yellow', '🟡 Soon (1-2 Days)'),
        ('green', '🟢 Flexible'),
    )

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    TYPE_CHOICES = (
        ('offer', 'Offer (Giving away)'),
        ('request', 'Request (Need help)'),
    )
    resource_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='offer')
    
    # New Quantity Fields for Partial Claims
    available_quantity = models.PositiveIntegerField(default=1, help_text="Number of items available")
    unit = models.CharField(max_length=50, default="items", help_text="e.g., kg, liters, packets, pieces")
    
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='green')
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    image = models.ImageField(upload_to='resources/', blank=True, null=True)
    
    DELIVERY_CHOICES = (
        ('pickup', 'Pickup Only'),
        ('dropoff', 'I can deliver'),
        ('both', 'Flexible (Pickup or Drop-off)'),
    )
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='pickup')

    pickup_window = models.CharField(max_length=200, help_text="e.g., 'Today 3PM-6PM'")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Removed simple 'claimed_by' in favor of Claim model for partial tracking
    # But we keep it temporarily if needed for queries, or property
    # claimed_by = models.ForeignKey(...) -> We rely on Claim model now

    def __str__(self):
        return f"{self.title} ({self.available_quantity} {self.unit} left)"

class Claim(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claims')
    quantity = models.PositiveIntegerField(default=1)
    claimed_at = models.DateTimeField(auto_now_add=True)
    
    # Verification
    import uuid
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.claimant.username} claimed {self.quantity} of {self.resource.title}"
