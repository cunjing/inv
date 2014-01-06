from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import account.views

urlpatterns = patterns('',
    url(r'^$', account.views.index),
    url(r'^admin/', include(admin.site.urls)),
)
