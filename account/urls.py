# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^sign_in/$', sign_in),
    url(r'^sign_up/$', sign_up),
    url(r'^logout/$', logout),
    url(r'^home/$', home),
)