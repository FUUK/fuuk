# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    # homepage redirect
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': reverse_lazy('flatpage', args=('thesis_offer/',))}),
    # pages
    url(r'^', include('fuuk.urls')),
)
