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
Go to the 'uos3' folder.

Run the following command:

`python3 manage.py runserver <IP>:<PORT>`

where <IP> is the desired IP address and <PORT> is the port number.

# Authors

Mohammed Nawabuddin

Charles West-Taylor
