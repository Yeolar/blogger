#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

python manage.py migrate
python manage.py createsuperuser
