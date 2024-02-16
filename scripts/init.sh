#!/bin/bash

# Vérifie si docker-compose est installé
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

# Configuration
domains=(intranet.cagiregaronnesalat.fr)
rsa_key_size=4096
data_path="./web/data/certbot"
email="service.informatique@cagiregaronnesalat.fr" # Remplacer par votre adresse email réelle
staging=1 # Utiliser 1 pour le mode test afin d'éviter d'atteindre les limites de requêtes

# Vérifie si des données existent déjà
if [ -d "$data_path" ]; then
  read -p "Existing data found for $domains. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

# Télécharge les paramètres TLS recommandés
if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

# Démarre les services avec docker-compose.prod.yml
echo "### Starting the docker-compose file"
docker-compose -f /home/webmaster/docker_intranet/docker-compose.prod.yml up -d

# Demande le certificat SSL pour les domaines
echo "### Requesting Let's Encrypt certificate for $domains ..."
# Convertit les domaines en arguments pour certbot
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Sélectionne l'argument email approprié
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Active le mode test si nécessaire
if [ $staging != "0" ]; then staging_arg="--staging"; fi

# Exécute certbot pour obtenir le certificat
docker-compose -f /home/webmaster/docker_intranet/docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo

# Arrête les services
echo "### Shutting down the docker-compose"
docker-compose -f /home/webmaster/docker_intranet/docker-compose.prod.yml down
