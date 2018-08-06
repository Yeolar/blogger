# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u6807\u9898')),
                ('slug', models.SlugField(verbose_name='\u522b\u540d', unique_for_date=b'publish')),
                ('text', models.TextField(verbose_name='\u6587\u672c')),
                ('publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('status', models.IntegerField(default=3, verbose_name='\u72b6\u6001', choices=[(1, '\u8349\u7a3f'), (2, '\u79c1\u6709'), (3, '\u516c\u5f00')])),
                ('author', models.ForeignKey(verbose_name='\u4f5c\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
                'db_table': 'note_posts',
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
                'get_latest_by': 'publish',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u79f0')),
                ('slug', models.SlugField(unique=True, verbose_name='\u522b\u540d')),
                ('publish', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0), verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('public', models.BooleanField(default=False, verbose_name='\u516c\u5f00', editable=False)),
            ],
            options={
                'ordering': ('-publish',),
                'db_table': 'note_topics',
                'verbose_name': '\u4e3b\u9898',
                'verbose_name_plural': '\u4e3b\u9898',
                'get_latest_by': 'publish',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(verbose_name='\u4e3b\u9898', blank=True, to='note.Topic', null=True),
        ),
    ]
