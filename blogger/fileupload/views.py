# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

import hashlib
import json
import os
import re
import urllib
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings

from ..util.decorators import superuser_required


fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'media'))


def handle_upload_file(prefix, file):
    now = datetime.now()
    dir = prefix + now.strftime('/%Y/%m/%d/')
    base, ext = os.path.splitext(file.name)
    name = hashlib.md5(base + str(now)).hexdigest()[:8] + ext
    path = dir + name
    url = settings.MEDIA_URL + path

    try:
        fs.save(path, file)
    except Exception as e:
        return {
            'uploaded': False,
            'error': {
                'message': '上传失败'
            },
        }
    return {
        'uploaded': True,
        'url': url,
    }


def handle_delete_file(path):
    if path and os.path.exists(settings.BASE_DIR + path):
        fs.delete(path)
        return {path: True}
    return {path: False}


@superuser_required
@csrf_exempt
def file_upload(request, **kwargs):
    json_data = {}
    if request.method == 'POST':
        if request.FILES:
            json_data.update(
                handle_upload_file('uploadfile', request.FILES['upload']))
        else:
            json_data.update({
                'uploaded': False,
                'error': {
                    'message': '上传失败'
                },
            })
    return HttpResponse(json.dumps(json_data), content_type='application/json')


@superuser_required
def file_delete(request, **kwargs):
    json_data = {}
    if request.method == 'DELETE':
        if request.GET:
            json_data.update({'files': [
                handle_delete_file(
                    urllib.unquote_plus(request.GET.get('p', '')))
            ]})
        else:
            json_data.update({'files': [
                {'none': False}
            ]})
    return HttpResponse(json.dumps(json_data), content_type='application/json')

