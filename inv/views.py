# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response('inv/index.html', {}, context_instance=RequestContext(request))


def site_help(request):
    return render_to_response('inv/index.html')


def contact(request):
    return render_to_response('inv/index.html')


def terms(request):
    return render_to_response('inv/index.html')


def privacy(request):
    return render_to_response('inv/index.html')


@csrf_exempt
def import_excel(request):
    data = {'info': ''}
    if request.method == 'POST':
        f = request.FILES['file']
        if 'xls' not in f.name and 'xlsx' not in f.name:
            data['info'] = 'file type must be excel!'
        else:
            pass
    return render_to_response('inv/import_excel.html', data)
