#!/bin/bash

# Ajustez les permissions ici
chown -R wagtail:wagtail /app/media

# Exécutez la commande CMD par défaut
exec "$@"
