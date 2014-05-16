# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^admin/import/questions/investee/$', import_investee_questions_from_excel),
)