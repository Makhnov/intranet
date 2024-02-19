#!/bin/bash

# Assurez-vous que tous les conteneurs sont en cours d'exécution
echo "Attente que tous les conteneurs soient lancés..."
sleep 10 # Ajustez ce temps selon le besoin

# 0. Lance la commande "docker-prod-db" (remplacez par la commande réelle si différente)
docker-prod-db

# 1. Donner des droits d'écriture
docker exec -u root web chmod -R u+w /usr/local/lib/python3.12/site-packages/wagtail/migrations/

# 2. Exécuter makemigrations
docker exec web python manage.py makemigrations

# 3. Exécuter migrate
docker exec web python manage.py migrate

# 4. Remise des droits d'écriture à la normale (root je crois ?)
docker exec -u root web chmod -R u-w /usr/local/lib/python3.12/site-packages/wagtail/migrations/

# 5. Collectstatic
docker exec web python manage.py collectstatic --noinput

# 6. Update_index
docker exec web python manage.py update_index

# 7. Assurez-vous que cette étape est ce que vous attendez pour "user wagtail"
# Si vous voulez changer des permissions ou exécuter une commande en tant que `wagtail`, ajoutez-la ici.

echo "Script de post-démarrage terminé."
