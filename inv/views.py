# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


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


def import_excel(request):
    return render_to_response('inv/index.html')
