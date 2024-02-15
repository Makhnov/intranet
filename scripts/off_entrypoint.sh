#!/bin/bash

echo 'entrypoint'

set -o errexit
set -o pipefail
set -o nounset

# Fonction pour vérifier si PostgreSQL est prêt
postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

# Appliquer les migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo 'Migrations appliquées'

# Création ou mise à jour du superutilisateur
{
    python manage.py createsuperuser --noinput \
        --username "${DJANGO_SUPERUSER_USERNAME}" \
        --email "${DJANGO_SUPERUSER_EMAIL}"
} || {
    echo "Le superutilisateur ${DJANGO_SUPERUSER_USERNAME} existe déjà."
}

# Modification du mot de passe du superutilisateur
script="
from django.contrib.auth import get_user_model;
User = get_user_model();
u = User.objects.get(username='${DJANGO_SUPERUSER_USERNAME}');
u.set_password('${DJANGO_SUPERUSER_PASSWORD}');
u.save();
"
echo "$script" | python manage.py shell

# Lancer le serveur Django avec nohup et rediriger les logs
exec python manage.py runserver 0.0.0.0:8000
