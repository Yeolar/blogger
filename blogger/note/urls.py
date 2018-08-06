# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from django.conf.urls import url

from .views import *


urlpatterns = [
    # operation
    url(r'^post/set/(?P<id>\d+)/$',
        post_set,
        name='note_set'
    ),
    url(r'^post/set/$',
        post_set,
        name='note_set'
    ),
    # date
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='note_detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        PostDayArchiveView.as_view(),
        name='note_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        PostMonthArchiveView.as_view(),
        name='note_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        PostYearArchiveView.as_view(),
        name='note_archive_year'
    ),
    # list
    url(r'^privates/$',
        PrivateListView.as_view(),
        name='note_private_list'
    ),
    url(r'^drafts/$',
        DraftListView.as_view(),
        name='note_draft_list'
    ),
    # topic
    url(r'^topics/(?P<slug>[-\w]+)/$',
        TopicDetailView.as_view(),
        name='note_topic_detail'
    ),
    url (r'^topics/$',
        TopicListView.as_view(),
        name='note_topic_list'
    ),
    # misc
    url(r'^search/$',
        search,
        name='note_search'
    ),
    url(r'^$',
        PostListView.as_view(),
        name='note_index'
    ),
]
