# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

from datetime import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from django.db.models import Q
from django.conf import settings

from .models import *
from .forms import *
from ..util.search.constants import STOP_WORDS_RE
from ..util.decorators import superuser_required


@superuser_required
def topic_set(request, id=None, **kwargs):
    if id:
        topic = Topic.objects.get(id=id)
    else:
        topic = Topic()

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)

        if form.is_valid():
            topic = form.save()
            return redirect(topic.get_absolute_url())
    else:
        form = TopicForm(instance=topic)

    return render_to_response(
            'note/topic_set.html',
            {'form': form, 'id': id},
            RequestContext(request))   # use for csrf


@superuser_required
def post_set(request, id=None, **kwargs):
    if id:
        post = Post.objects.get(id=id)
    else:
        post = Post()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post, author=request.user)

        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post, author=request.user)
        form.fields['topic'].queryset = Topic.objects.all()

    return render_to_response(
            'note/post_set.html',
            {'form': form, 'id': id},
            RequestContext(request))   # use for csrf


class TopicListView(ListView):

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.topics = Topic.objects.all()
        else:
            self.topics = Topic.objects.public()
        return self.topics

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': self.topics[:5],
        })
        return context


class TopicDetailView(ListView):

    paginate_by = getattr(settings, 'NOTE_PAGESIZE', 20)
    template_name = 'note/topic_detail.html'

    def get_queryset(self):
        self.topic = get_object_or_404(
                Topic, slug__iexact=self.kwargs['slug'])
        if self.request.user.is_superuser:
            return self.topic.post_set.published()
        else:
            return self.topic.post_set.public()

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            topics = Topic.objects.all()
        else:
            topics = Topic.objects.public()
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': topics[:5],
            'topic': self.topic
        })
        return context


class PostListView(ListView):

    paginate_by = getattr(settings, 'NOTE_PAGESIZE', 20)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.public()

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            topics = Topic.objects.all()
        else:
            topics = Topic.objects.public()
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': topics[:5],
        })
        return context


class PrivateListView(ListView):

    paginate_by = getattr(settings, 'NOTE_PAGESIZE', 20)
    template_name = 'note/private_list.html'

    @method_decorator(superuser_required)
    def dispatch(self, *args, **kwargs):
        return super(PrivateListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Post.objects.private()

    def get_context_data(self, **kwargs):
        context = super(PrivateListView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': Topic.objects.all()[:5],
        })
        return context


class DraftListView(ListView):

    paginate_by = getattr(settings, 'NOTE_PAGESIZE', 20)
    template_name = 'note/draft_list.html'

    @method_decorator(superuser_required)
    def dispatch(self, *args, **kwargs):
        return super(DraftListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Post.objects.draft()

    def get_context_data(self, **kwargs):
        context = super(DraftListView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': Topic.objects.all()[:5],
        })
        return context


class PostYearArchiveView(YearArchiveView):

    date_field = 'publish'
    make_object_list = True

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.published()
        else:
            return Post.objects.public()

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            topics = Topic.objects.all()
        else:
            topics = Topic.objects.public()
        context = super(PostYearArchiveView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': topics[:5],
        })
        return context


class PostMonthArchiveView(MonthArchiveView):

    date_field = 'publish'
    month_format = '%m'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.published()
        else:
            return Post.objects.public()

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            topics = Topic.objects.all()
        else:
            topics = Topic.objects.public()
        context = super(PostMonthArchiveView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': topics[:5],
        })
        return context


class PostDayArchiveView(DayArchiveView):

    date_field = 'publish'
    month_format = '%m'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.published()
        else:
            return Post.objects.public()

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            topics = Topic.objects.all()
        else:
            topics = Topic.objects.public()
        context = super(PostDayArchiveView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': topics[:5],
        })
        return context


class PostDetailView(DateDetailView):

    month_format = '%m'
    date_field = 'publish'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()  # show draft for preview
        else:
            return Post.objects.public()

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            topics = Topic.objects.all()
        else:
            topics = Topic.objects.public()
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'topic_list': topics[:5],
        })
        return context


def search(request, paginate_by=10,
        template_name='note/post_search.html', **kwargs):
    page_size = getattr(settings,'SEARCH_PAGESIZE', paginate_by)

    if request.GET:
        if request.user.is_superuser:
            posts = Post.objects.published()
            topics = Topic.objects.all()
        else:
            posts = Post.objects.public()
            topics = Topic.objects.public()

        context = {
            'topic_list': topics[:5],
        }

        vague_terms = True
        stop_word_list = STOP_WORDS_RE
        search_terms = '%s' % request.GET['q']
        search_term_list = search_terms.split()
        cleaned_search_term_list = []
        for search_term in search_term_list:
            cleaned_search_term = stop_word_list.sub('', search_term)
            cleaned_search_term = cleaned_search_term.strip()
            if len(cleaned_search_term) != 0:
                cleaned_search_term_list.append(cleaned_search_term)
                posts = posts.filter(
                        Q(title__icontains=cleaned_search_term) |
                        Q(author__username__icontains=cleaned_search_term) |
                        Q(text__icontains=cleaned_search_term))
                vague_terms = False

        if not vague_terms:
            if len(posts) != 0:
                paginator = Paginator(posts, page_size)
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                try:
                    objects = paginator.page(page)
                except EmptyPage, InvalidPage:
                    objects = paginator.page(paginator.num_pages)
                context.update({
                    'paged_objects': objects,
                    'search_terms': search_terms,
                    'cleaned_search_terms': ' '.join(cleaned_search_term_list)
                })
            else:
                message = u'结果未找到。'
                context.update({'message': message})
        else:
            message = u'搜索条件太简单，请调整。'
            context.update({'message': message})

    return render_to_response(template_name, context, RequestContext(request))
