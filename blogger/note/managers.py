# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from datetime import datetime

from django.db.models import Manager


class TopicManager(Manager):

    def public(self):
        return self.get_queryset().filter(public__exact=True)


class PostManager(Manager):

    def published(self):
        return self.get_queryset().filter(
                status__gte=2, publish__lte=datetime.now())

    def draft(self):
        return self.get_queryset().filter(
                status__exact=1, publish__lte=datetime.now())

    def private(self):
        return self.get_queryset().filter(
                status__exact=2, publish__lte=datetime.now())

    def public(self):
        return self.get_queryset().filter(
                status__exact=3, publish__lte=datetime.now())
