import random
from django.core.management.base import BaseCommand
from resources.models import Resource

class Command(BaseCommand):
    help = 'Randomizes the location of all resources to be around Pune, Maharashtra'

    def handle(self, *args, **kwargs):
        # Pune Center
        PUNE_LAT = 18.5204
        PUNE_LON = 73.8567
        
        # Spread (approx 0.05 deg is roughly 5km radius)
        SPREAD = 0.05

        resources = Resource.objects.all()
        count = 0
        
        for resource in resources:
            # Generate random offset
            lat_offset = random.uniform(-SPREAD, SPREAD)
            lon_offset = random.uniform(-SPREAD, SPREAD)
            
            resource.latitude = PUNE_LAT + lat_offset
            resource.longitude = PUNE_LON + lon_offset
            resource.save()
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} resources with locations around Pune.'))
