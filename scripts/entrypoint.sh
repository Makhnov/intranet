#!/bin/bash

# Utiliser wait-for-it pour s'assurer que la DB est prête
/usr/local/bin/wait-for-it.sh db:5432 --timeout=30 -- echo "La base de données est prête."

# Qui suis-je ?
echo "Management de $(whoami)"

# Exécuter les commandes Django
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py update_index

echo "Démarrage de l'application..."
exec "$@"
