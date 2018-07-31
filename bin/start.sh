#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

uwsgi --ini /home/yeolar/app/blogger/blogger/uwsgi.ini &
