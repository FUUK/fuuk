# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    # homepage redirect
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/thesis_offer'}),
    # pages
    url(r'^', include('fuuk.urls')),
)
