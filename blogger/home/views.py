# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.views.generic.list import ListView
from django.conf import settings

from ..note.models import Post, Topic


class HomePageView(ListView):

    paginate_by = getattr(settings, 'HOME_PAGESIZE', 5)
    template_name = 'home/index.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.published()
        else:
            return Post.objects.public()
