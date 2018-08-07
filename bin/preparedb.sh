#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

# CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL privileges ON database.* TO 'user'@'localhost';

python manage.py migrate
python manage.py createsuperuser
