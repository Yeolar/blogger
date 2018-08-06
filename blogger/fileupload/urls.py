# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^upload/$',
        file_upload,
        name='file_upload'
    ),
    url(r'^delete/$',
        file_delete,
        name='file_delete'
    ),
]
