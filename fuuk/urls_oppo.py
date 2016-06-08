# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.simple import redirect_to

urlpatterns = [
    # homepage redirect
    url(r'^$', redirect_to, {'url': reverse_lazy('flatpage', args=('thesis_offer/',))}),
    # pages
    url(r'^', include('fuuk.urls')),
]
