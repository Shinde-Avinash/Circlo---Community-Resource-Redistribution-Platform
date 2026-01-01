from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Resets all users location to Pune default'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Pune Center
        PUNE_LAT = 18.5204
        PUNE_LON = 73.8567
        
        users = User.objects.all()
        count = 0
        for user in users:
            user.latitude = PUNE_LAT
            user.longitude = PUNE_LON
            user.save()
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} users to Pune location.'))
