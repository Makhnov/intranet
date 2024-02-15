from django.core.management.base import BaseCommand
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = 'Génère un fichier iCal avec des événements fictifs'

    def handle(self, *args, **kwargs):
        # Création du calendrier
        cal = Calendar()

        # Ajout de quelques événements fictifs en décembre 2023
        for i in range(1, 4):
            event = Event()
            event.add('summary', f'Événement Exemple {i}')
            start_date = datetime(2023, 12, i * 5, 10, 0, 0, tzinfo=pytz.UTC)  # événements le 5, 10 et 15 décembre
            end_date = start_date + timedelta(hours=2)  # Durée de 2 heures pour chaque événement
            event.add('dtstart', start_date)
            event.add('dtend', end_date)
            event.add('dtstamp', start_date)
            event['uid'] = f'event-example-{i}@monsite.com'
            event.add('priority', 5)

            cal.add_component(event)

        # Enregistrement du fichier .ics
        ics_file_path = 'calendrier_exemple.ics'
        with open(ics_file_path, 'wb') as ics_file:
            ics_file.write(cal.to_ical())

        self.stdout.write(self.style.SUCCESS('Fichier iCal généré avec succès'))
