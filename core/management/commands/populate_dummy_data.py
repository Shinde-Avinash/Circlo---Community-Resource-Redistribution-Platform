import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resources.models import Resource
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')
        
        # Create Users
        users_data = [
            {'username': 'donor_john', 'role': 'donor', 'lat': 12.9716, 'long': 77.5946}, # Bangalore Center
            {'username': 'donor_sara', 'role': 'business', 'lat': 12.9780, 'long': 77.6320}, # Indiranagar
            {'username': 'recipient_jane', 'role': 'recipient', 'lat': 12.9560, 'long': 77.5870}, # Lalbagh
            {'username': 'ngo_help', 'role': 'organization', 'lat': 12.9352, 'long': 77.6245}, # Koramangala
            {'username': 'mod_admin', 'role': 'moderator', 'lat': 12.9716, 'long': 77.5946},
        ]

        for u in users_data:
            user, created = User.objects.get_or_create(username=u['username'], email=f"{u['username']}@example.com")
            user.set_password('password123')
            user.role = u['role']
            user.latitude = u['lat']
            user.longitude = u['long']
            user.is_verified = True
            user.save()
            self.stdout.write(f"Created/Updated user: {u['username']}")

        # Create Resources
        donors = User.objects.filter(role__in=['donor', 'business'])
        categories = ['food', 'clothing', 'furniture', 'books']
        urgencies = ['red', 'yellow', 'green']
        
        # Resources focused around Bangalore
        locations = [
            (12.9716, 77.5946), (12.9780, 77.6320), (12.9250, 77.5890), 
            (12.9100, 77.6000), (12.9900, 77.5500)
        ]

        for i in range(20):
            donor = random.choice(donors)
            lat, long = random.choice(locations)
            # Add some jitter to coords
            lat += random.uniform(-0.02, 0.02)
            long += random.uniform(-0.02, 0.02)
            
            urgency = random.choice(urgencies)
            res = Resource.objects.create(
                donor=donor,
                title=f"Surplus {random.choice(categories)} item {i}",
                description="This is a dummy resource description for testing purposes.",
                category=random.choice(categories),
                quantity=f"{random.randint(1, 10)} units",
                urgency=urgency,
                latitude=lat,
                longitude=long,
                pickup_window="Today 4PM - 7PM",
            )
            self.stdout.write(f"Created resource: {res.title} ({urgency})")

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data'))
