# Telecommand server
The server for sending telecommands to UoS³ CubeSat

## Requirements
+ [Django](https://www.djangoproject.com/), version 2.0+
+ [Python](https://www.python.org/), version 3.x preferred
+ [NGINX](https://nginx.org), version 1.16+

## Install
1. _Requires an Ubuntu Server install on the machine first (Bionic or above)._
2. _Requires a network connection and a way for the user to remotely login._

Download the official Django package for Ubuntu.

Install the Django package on the machine.

Download and install the required NGINX package.

## Run
Go to the `uos3/uos3/` folder.

Run the following command:

`python3 manage.py runserver <IP>:<PORT>`

where _IP_ is the desired IP address and _PORT_ is the port number.

## NGINX server setup
The NGINX server can be configured from the `init.sh` shell script located at `server-init/init.sh`.

This script sets up a test server with credentials-based authentication.

It can also be used to set up SSL/TLS security by generating certificates. To do so, simply run the script with the `-ssl` flag.

First make sure that there are certain files in a subfolder called `SECRETS/`:

+ `AUTH_USERS` which contains a username on each line. No spaces in the names.
+ `SSL_DIR` which contains the path to the directory where the user credentials (and optional certificates) will be stored.
+ TODO: `SSL_STRONG_CONF` which contains the parameters for strong SSL/TLS security (if certificates are needed).

Once the server is ready and moved over to production, make sure that it is linked to the Django server using e.g. uWSGI.

## Security checks before entering production
Once the production server is ready, make sure to do the following in the `uos3/uos3/settings.py` file:
1. **Make sure that SECRET_KEY is hidden.**
2. **Make sure that the DEBUG flag is disabled.**
3. **Make sure that ALLOWED_HOSTS is set so that only authorised hosts can connect.**

## Notes on Cloning
1. The Django server production secret key needs to be stored in the `uos3/uos3/secrets.py` file. As an example, the contents of the file can be `secret_key = <KEY>` where _KEY_ is the secret key string.
2. Make sure that the database file in the `uos3` folder is copied over from the relevant UoS³ project cloud storage.

# Authors

Mohammed Nawabuddin

Charles West-Taylor

Hubert Khoo Hui Boo
