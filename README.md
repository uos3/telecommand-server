# Telecommand server
The server for sending telecommands to UoS³ CubeSat

## Requirements
+ [Django](https://www.djangoproject.com/), version 2.0+
+ [Python](https://www.python.org/), version 3.x preferred

## Install
1. _Requires an Ubuntu Server install on the machine first (Bionic or above)._
2. _Requires an Apache or NGINX server install on the machine first._
3. _Requires a network connection and a way for the user to remotely login._

Download the official Django package for Ubuntu.

Install the Django package on the machine.

## Run
Go to the `uos3/uos3/` folder.

Run the following command:

`python3 manage.py runserver <IP>:<PORT>`

where 'IP' is the desired IP address and 'PORT' is the port number.

## Link with Apache / NGINX server
_TODO_

## Security checks before entering production
Once the production server is ready, make sure to do the following in the `uos3/uos3/settings.py` file:
1. **Make sure that SECRET_KEY is hidden.**
2. **Make sure that the DEBUG flag is disabled.**
3. **Make sure that ALLOWED_HOSTS is set so that only authorised hosts can connect.**

## Notes on Cloning
1. The Django server production secret key needs to be stored in the `uos3/uos3/secrets.py` file. As an example, the contents of the file can be `secret_key = <KEY>` where _<KEY>_ is the secret key string.
2. Make sure that the database file in the `uos3` folder is copied over from the relevant UoS³ project cloud storage.

# Authors

Mohammed Nawabuddin

Charles West-Taylor

Hubert Khoo Hui Boo
