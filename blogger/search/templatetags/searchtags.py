# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

import re
from unicodedata import east_asian_width

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

html_tag_pattern = re.compile(r'<[^>]+>')


def get_cut_len(line_num):
    return line_num * 100 - 10


def get_cut_text(text, start, n):
    summary = ''
    i = 0
    p = start
    end = len(text)
    while i < n and p < end:
        c = text[p]
        summary += c
        if east_asian_width(c) in ('F', 'W'):
            i += 2
        else:
            i += 1
        p += 1
    return (('...' if (start > 0) else '') + summary +
            ('...' if (p < end) else ''))


def get_search_summary(html, search_terms, line_num):
    search_term_list = search_terms.split()
    text = html_tag_pattern.sub('', html)
    lower_text = text.lower()
    start = 0
    for term in search_term_list:
        i = lower_text.find(term.lower())
        if i != -1:
            start = i
    start = max(start - 20, 0)
    return get_cut_text(text, start, get_cut_len(line_num))


@register.filter
@stringfilter
def cut_text(text, n):
    return get_cut_text(text, 0, n)
cut_text.is_safe = True


@register.filter
@stringfilter
def search_summary(html, search_terms):
    return get_search_summary(html, search_terms, 3)
search_summary.is_safe = True


@register.filter
@stringfilter
def singleline_search_summary(html, search_terms):
    return get_search_summary(html, search_terms, 1)
search_summary.is_safe = True
