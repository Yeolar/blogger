#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

HOST=$1

echo "deploy to ["$1":~/app/blogger/]"

rsync -av                   \
    --exclude=settings.py   \
    --exclude=*.pyc         \
    bin                     \
    blogger                 \
    static                  \
    templates               \
    manage.py               \
    LICENSE                 \
    README.md               \
    $HOST:~/app/blogger/
