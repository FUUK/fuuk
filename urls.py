# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language


admin.autodiscover()

urlpatterns = patterns('',
    # homepage with news
    url(r'^$', 'people.views.news', name="homepage"),
    # pages
    url(r'^people/', include('people.urls')),
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # languages
    url(r'^setlang/$', csrf_exempt(set_language), name="set_language"),
    # media
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
