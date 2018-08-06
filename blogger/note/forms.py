# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

from django.forms import ModelForm
from django.forms import HiddenInput, TextInput, Select, Textarea

from .models import *


class TopicForm(ModelForm):

    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = Topic
        fields = ('name', 'slug', 'text', 'publish')
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': u'主题',
                    'onkeyup': 'calcHash()'
                }),
            'slug': HiddenInput(attrs={'class': 'form-control input-sm'}),
            'text': Textarea(attrs={'class': 'form-control input-sm'}),
            'publish': TextInput(attrs={'class': 'form-control input-sm'}),
        }


class PostForm(ModelForm):

    required_css_class = 'required'
    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.author = self.author
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Post
        fields = ('title', 'slug', 'text', 'publish', 'status', 'topic')
        widgets = {
            'title': TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': u'标题',
                    'onkeyup': 'calcHash()'
                }),
            'slug': HiddenInput(attrs={'class': 'form-control input-sm'}),
            'text': Textarea(attrs={'class': 'form-control input-sm'}),
            'publish': TextInput(attrs={'class': 'form-control input-sm'}),
            'status': Select(attrs={'class': 'form-control input-sm'}),
            'topic': Select(attrs={'class': 'form-control input-sm'}),
        }
