# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.contrib import admin
from .models import *


class TopicAdmin(admin.ModelAdmin):
    list_display        = ('name', 'publish', 'public')
    list_filter         = ('publish', 'public')
    list_per_page       = 50
    search_fields       = ('name', 'text')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets           = ((None, {
        'fields': (
            ('name', 'slug'),
             'text',
             'publish')
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
