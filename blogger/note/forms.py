# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

from django.forms import ModelForm, TextInput, Select, Textarea

from .models import *


class PostForm(ModelForm):

    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = Post
        fields = (
            'title', 'slug', 'author', 'text', 'publish', 'status', 'topic'
        )
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control input-sm',
                       'onkeyup': 'calcHash()'}),
            'slug': TextInput(attrs={'class': 'form-control input-sm'}),
            'author': Select(attrs={'class': 'form-control input-sm'}),
            'text': Textarea(attrs={'class': 'form-control input-sm'}),
            'publish': TextInput(attrs={'class': 'form-control input-sm'}),
            'status': Select(attrs={'class': 'form-control input-sm'}),
            'topic': Select(attrs={'class': 'form-control input-sm'}),
        }
