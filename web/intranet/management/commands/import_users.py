import json
import os
from django.conf import settings
from users.models import User
from utils.widgets import CiviliteListe, FonctionsConseilListe
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import users from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, '../files/ignore/users_credentials.json')

        with open(file_path, 'r', encoding='utf-8') as file:
            users_data = json.load(file)

        for user_info in users_data:
            civility_value = user_info['civility']
            if civility_value == "Madame":
                civility = CiviliteListe.F
            elif civility_value == "Monsieur":
                civility = CiviliteListe.H
            else:
                civility = CiviliteListe.N
            
            # Utiliser update_or_create pour créer ou mettre à jour l'utilisateur
            user, created = User.objects.update_or_create(
                username=user_info['identifiant'],
                defaults={
                    'first_name': user_info['prenom'],
                    'last_name': user_info['nom'],
                    'email': user_info['mail'],
                    'civility': civility,
                    'function_council': FonctionsConseilListe.MEMBRE,
                    'is_superuser': False,
                    'is_staff': False,
                    'is_active': False
                }
            )
            user.set_password(user_info['mot de passe'])
            user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated user {user.username}'))
