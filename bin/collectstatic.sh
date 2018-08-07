#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

cd fe

if [ ! -d node_modules ]; then
    npm install -g grunt-cli
    npm install
fi

grunt deploy
cd -

python manage.py collectstatic
