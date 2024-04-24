from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accompte.models import CGSUserProfile

class Command(BaseCommand):
    help = 'Creates CGSUserProfile for users who do not have one'

    def handle(self, *args, **options):
        UserModel = get_user_model()
        users_without_profiles = UserModel.objects.filter(cgs_userprofile__isnull=True)
        for user in users_without_profiles:
            CGSUserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created profile for {user.username}'))
