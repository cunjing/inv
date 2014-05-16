# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import inv.views
import account.urls
import matching.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', inv.views.index),
    url(r'^help$', inv.views.site_help),
    url(r'^contact$', inv.views.contact),
    url(r'^terms$', inv.views.terms),
    url(r'^privacy$', inv.views.privacy),
)
urlpatterns += account.urls.urlpatterns
urlpatterns += matching.urls.urlpatterns
urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))
