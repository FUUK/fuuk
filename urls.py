# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from people.models import Article
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'front_page.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^people/', include('people.urls')),
    url(r'^articles/$', 'people.views.article_list'),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
