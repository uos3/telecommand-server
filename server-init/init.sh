#!/bin/sh

SSL_DIR=$( cat "`dirname $0`/SSL_DIR" )
[ -z $SSL_DIR ] && {
  echo "FATAL: You forgot to add the secret UoS3 SSL dir path! Exiting..."
  exit 1
}

echo "Hi!\nInitiating UoS3 server config\n"

sudo apt-get update
sudo apt-get -y install nginx openssl

if [ ! -d $SSL_DIR ]; then
  echo "\nUoS3 SSL directory does not exist. Creating..."
  sudo mkdir -p $SSL_DIR
  [ ! -d $SSL_DIR ] && {
    echo "FATAL: Cannot create UoS3 SSL directory! Exiting..."; exit 1;
  } || echo "Created\n"
else
    echo "\nFound UoS3 SSL directory\n"
fi

if [ ! -f "${SSL_DIR}/uos3.key" -o ! -f "${SSL_DIR}/uos3.crt" ]; then
  echo "SSL cert is required. Creating..."
  sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ${SSL_DIR}/uos3.key -out ${SSL_DIR}/uos3.crt
  [ ! -f "${SSL_DIR}/uos3.key" -o ! -f "${SSL_DIR}/uos3.crt" ] && {
    echo "FATAL: Cannot create SSL cert! Exiting..."; exit 1;
  } || echo "Created\n"
else
    echo "Found existing SSL cert\n"
fi
