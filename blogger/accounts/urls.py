# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^login/',
        login_site,
        name='login_site'
    ),
    url(r'^logout/',
        logout_site,
        name='logout_site'
    ),
]
