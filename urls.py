# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language
from datetime import date
from people.models import Grant, Thesis
from django.db.models import Q

admin.autodiscover()

urlpatterns = patterns('',
    #TODO: homepage should only exist as flatpage
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'front_page.html'}, name="homepage"),
    # pages
    url(r'^people/', include('people.urls')),
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # languages
    url(r'^setlang/$', csrf_exempt(set_language), name="set_language"),
    # media
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
