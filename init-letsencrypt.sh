#!/bin/bash

domains=(notcheapnot2expensive.com www.notcheapnot2expensive.com)
email="your-email@example.com" # Change this to your email
staging=0 # Set to 1 if you're testing

data_path="./certbot"
rsa_key_size=4096

if [ -d "$data_path" ]; then
  read -p "Existing data found. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

mkdir -p "$data_path/conf/live/$domains"
docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot

echo "### Starting nginx ..."
docker-compose up --force-recreate -d nginx

echo "### Requesting Let's Encrypt certificate for $domains ..."
docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --email $email \
    --agree-tos \
    --no-eff-email \
    --staging \
    -d ${domains[0]} -d ${domains[1]}" certbot

echo "### Reloading nginx ..."
docker-compose exec nginx nginx -s reload 