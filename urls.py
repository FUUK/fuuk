# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from datetime import date
from people.models import Grant
from django.db.models import Q

admin.autodiscover()

grants = {
    'queryset': Grant.objects.filter(end__gte=date.today().year),
    'template_name': 'grant_list.html',
    'template_object_name': 'grants',
    'extra_context': {'grants2_list': Grant.objects.filter(Q(end__gte=(date.today().year) - 2), Q(end__lt=date.today().year))},
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'front_page.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^people/', include('people.urls')),
    url(r'^articles/$', 'people.views.article_list'),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list'),
    url(r'^grants/$', 'django.views.generic.list_detail.object_list', grants),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
