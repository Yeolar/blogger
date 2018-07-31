#!/usr/bin/env sh
#
# Copyright 2018 Yeolar
#

# execute ``workon app`` first.

uwsgi --reload /tmp/blogger-master.pid
