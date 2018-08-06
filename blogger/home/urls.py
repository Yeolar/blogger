# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^$',
        HomePageView.as_view(),
        name='home_index'
    ),
]
