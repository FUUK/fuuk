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


thesis = {
    'queryset': Thesis.objects.filter(annotation__isnull=False),
    'template_name': 'thesis_defend_page.html',
    'template_object_name': 'thesis',
    'extra_context': {'years_list': Thesis.objects.filter(annotation__isnull=False).values_list('year', flat=True).distinct(), 'type_list': Thesis.objects.filter(annotation__isnull=False).values_list('type').distinct()},
}

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
    url(r'^articles/$', 'people.views.article_list'),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list'),
#    url(r'^grants/$', 'django.views.generic.list_detail.object_list', grants),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^thesis_defend/$', 'django.views.generic.list_detail.object_list', thesis),
)
