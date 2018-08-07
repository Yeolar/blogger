#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

# CREATE DATABASE blogger DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
# CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL privileges ON blogger.* TO 'user'@'localhost';

python manage.py migrate
python manage.py createsuperuser
