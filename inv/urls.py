from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views
import account.urls

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += account.urls.urlpatterns
