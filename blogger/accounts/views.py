# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

import urllib

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout


def redirect_url(request):
    """Get appropriate url for redirect"""

    next = request.POST.get('next')
    if next:
        return urllib.unquote(next)
    return request.META.get('HTTP_REFERER', '/')


def login_site(request):
    """Logs in user and redirects to appropriate location"""

    if not request.user.is_anonymous():
        return redirect(redirect_url(request))

    response = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(redirect_url(request))
            else:
                response['error'] = u'用户名或密码错误！'
        else:
            response['error'] = u'用户名或密码未填。'
    response['next'] = request.REQUEST.get('next', '/')

    return render_to_response('accounts/login.html',
            response, RequestContext(request))


def logout_site(request):
    logout(request)
    return redirect(redirect_url(request))

