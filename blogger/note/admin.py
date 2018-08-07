# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.contrib import admin
from .models import *


class TopicAdmin(admin.ModelAdmin):
    list_display        = ('name', 'weight', 'public')
    list_filter         = ('weight', 'public')
    list_per_page       = 50
    search_fields       = ('name', 'desc')
    fieldsets           = ((None, {
        'fields': (
             'name',
             'desc',
             'contents',
             'weight')
        }),)

admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'author', 'publish', 'status',
                           'topic', 'link')
    list_filter         = ('publish', 'status')
    list_per_page       = 50
    search_fields       = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets           = ((None, {
        'fields': (
            ('title', 'slug'),
             'text',
             'author',
             'topic',
             'status',
             'publish')
        }),)

admin.site.register(Post, PostAdmin)
