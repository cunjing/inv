from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import account.views

urlpatterns = patterns('',
    url(r'^$', account.views.index),
    url(r'^sign_in/', account.views.sign_in),
    url(r'^sign_up/', account.views.sign_up),
    url(r'^admin/', include(admin.site.urls)),
)
