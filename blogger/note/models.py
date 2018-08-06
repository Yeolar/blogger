# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from BeautifulSoup import BeautifulSoup

from .managers import TopicManager, PostManager


class Topic(models.Model):

    name = models.CharField(u'名称', max_length=100)
    slug = models.SlugField(u'别名', unique=True)
    text = models.TextField(u'文本', blank=True)
    publish = models.DateTimeField(u'发布时间', default=datetime.min)
    public = models.BooleanField(u'公开', editable=False, default=False)

    objects = TopicManager()

    class Meta:
        verbose_name = u'主题'
        verbose_name_plural = u'主题'
        db_table = 'note_topics'
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('note_topic_detail', None, {'slug': self.slug})


class Post(models.Model):

    STATUS_CHOICES = ((1, u'草稿'), (2, u'私有'), (3, u'公开'))

    title = models.CharField(u'标题', max_length=200)
    slug = models.SlugField(u'别名', unique_for_date='publish')
    author = models.ForeignKey(User, verbose_name=u'作者')
    text = models.TextField(u'文本')
    publish = models.DateTimeField(u'发布时间', default=datetime.now)
    status = models.IntegerField(u'状态', choices=STATUS_CHOICES, default=3)
    topic = models.ForeignKey(Topic,
            verbose_name=u'主题', blank=True, null=True)

    objects = PostManager()

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章'
        db_table = 'note_posts'
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    def readable_str(self):
        return u'%4s:%s (%s)' % (self.id, self.get_absolute_url(), self.title)

    @permalink
    def get_absolute_url(self):
        return ('note_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%m'),
            'day': self.publish.strftime('%d'),
            'slug': self.slug
        })

    def link(self):
        return '<a href="%s">%s</a>' % (self.get_absolute_url(), u'查看')
    link.allow_tags = True

    @property
    def html_short(self):
        return unicode(BeautifulSoup(self.text[:100]))

    def get_previous_post_su(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_previous_post(self):
        return self.get_previous_by_publish(status__exact=3)

    def get_next_post_su(self):
        return self.get_next_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__exact=3)

    def get_previous_topic_post_su(self):
        return self.get_previous_by_publish(status__gte=2, topic=self.topic)

    def get_previous_topic_post(self):
        return self.get_previous_by_publish(status__exact=3, topic=self.topic)

    def get_next_topic_post_su(self):
        return self.get_next_by_publish(status__gte=2, topic=self.topic)

    def get_next_topic_post(self):
        return self.get_next_by_publish(status__exact=3, topic=self.topic)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.topic:
            if self.topic.publish < self.publish:
                self.topic.publish = self.publish
            self.topic.public = (len(self.topic.post_set.public()) != 0)
            self.topic.save()

    def delete(self, *args, **kwargs):
        if self.topic:
            if self.topic.publish == self.publish:
                post = self.get_previous_topic_post()
                if post:
                    self.topic.publish = post.publish
                else:
                    self.topic.publish = datetime.min
            if self.status == 3:
                self.topic.public = (len(self.topic.post_set.public()) > 1)
            self.topic.save()
        super(Post, self).delete(*args, **kwargs)

