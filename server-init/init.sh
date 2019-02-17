#!/bin/sh

echo "Hi!\nInitiating UoS3 server config\n"

SSL_DIR=$( cat "`dirname $0`/SSL_DIR" )
[ -z $SSL_DIR ] && {
  echo "FATAL: You forgot to add the secret UoS3 SSL dir path! Exiting..."
  exit 1
}
[ ! -f "`dirname $0`/SSL_STRONG_CONF" ] && {
  SSL_STRONG_CONF=""
  echo "You have not specified strong SSL configs. Leaving at weak SSL for now."
} || {
  SSL_STRONG_CONF="`dirname $0`/SSL_STRONG_CONF"
}

if ! which nginx > /dev/null 2>&1; then
  echo "nginx is not installed! Installing...\n"
  sudo apt-get update && sudo apt-get -y install nginx
fi
if ! which nginx > /dev/null 2>&1; then
  echo "\nFATAL: nginx is not installed! Exiting..."
  exit 1
fi
if ! which openssl > /dev/null 2>&1; then
  echo "OpenSSL is not installed! Installing...\n"
  sudo apt-get update && sudo apt-get -y install openssl
fi
if ! which openssl > /dev/null 2>&1; then
  echo "\nFATAL: OpenSSL is not installed! Exiting..."
  exit 1
fi

if [ ! -d $SSL_DIR ]; then
  echo "\nUoS3 SSL directory does not exist. Creating..."
  sudo mkdir -p $SSL_DIR
  [ ! -d $SSL_DIR ] && {
    echo "FATAL: Cannot create UoS3 SSL directory! Exiting..."; exit 1;
  } || echo "Created\n"
else
  echo "\nFound UoS3 SSL directory\n"
fi

if [ ! -f "${SSL_DIR}/private/uos3.key" -o ! -f "${SSL_DIR}/certs/uos3.crt" ]; then
  echo "SSL cert is required. Creating..."
  echo "This step is important. Confirm that you know what you are doing. (y/N)"
  read PROMPT
  [ "$PROMPT" = "y" -o "$PROMPT" = "Y" ] && {
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout ${SSL_DIR}/private/uos3.key -out ${SSL_DIR}/certs/uos3.crt
    sudo openssl dhparam -out ${SSL_DIR}/dhparam.pem 4096
  } || {
    echo "Aborted. Goodbye."
    exit 1
  }
  [ ! -f "${SSL_DIR}/private/uos3.key" -o ! -f "${SSL_DIR}/certs/uos3.crt" ] && {
    echo "\nFATAL: Cannot create SSL cert! Exiting..."; exit 1;
  } || echo "\nCreated\n"
else
  echo "Found existing SSL cert\n"
fi

echo "Remaking SSL snippets..."
[ -d ${SSL_DIR}/snippets ] && sudo rm -rfv ${SSL_DIR}/snippets
sudo mkdir -pv ${SSL_DIR}/snippets
SNIP_CRT_POINT="${SSL_DIR}/snippets/uos3-cert-pointer.conf"
sudo touch $SNIP_CRT_POINT
echo "ssl_certificate ${SSL_DIR}/certs/uos3.crt" | sudo tee -a $SNIP_CRT_POINT
echo "ssl_certificate_key ${SSL_DIR}/private/uos3.key" | sudo tee -a $SNIP_CRT_POINT
[ ! "$SSL_STRONG_CONF" = "" ] && {
  SNIP_STRONG_SSL="${SSL_DIR}/snippets/uos3-strong-ssl.conf"
  sudo touch $SNIP_STRONG_SSL
  cat $SSL_STRONG_CONF | sudo tee -a $SNIP_STRONG_SSL
}
echo "SSL snippets remade\n"

echo "Enabling SSL in nginx config..."
echo "TODO"
echo "Completed! Have a nice day!"
