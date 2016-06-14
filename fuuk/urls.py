# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # languages
    url(r'^setlang/$', csrf_exempt(set_language), name="set_language"),
    # media
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
    # pages
    url(r'^', include('fuuk.people.urls')),
    url(r'^(?P<url>.*)$', flatpage, name='flatpage'),
]
