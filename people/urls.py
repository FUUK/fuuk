# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from people.models import Person
from django.db.models import Q

admin.autodiscover()

phds = {
    'queryset': Person.objects.filter(type__icontains='PHD').order_by('last_name'),
    'template_name': 'people_list.html',
    'template_object_name': 'people',
    'extra_context': {"text": "Doktorandi"},
}

staff = {
    'queryset': Person.objects.filter(type__icontains='STAFF').order_by('last_name'),
    'template_name': 'people_list.html',
    'template_object_name': 'people',
    'extra_context': {"text": "Členové oddělení"},
}

students = {
    'queryset': Person.objects.filter(Q(type__icontains='MGR') | Q(type__icontains='BC')).order_by('last_name'),
    'template_name': 'student_list.html',
    'template_object_name': 'people',
}

urlpatterns = patterns('',
    url(r'^phd/$', 'django.views.generic.list_detail.object_list', phds),
    url(r'^staff/$', 'django.views.generic.list_detail.object_list', staff),
    url(r'^students/$', 'django.views.generic.list_detail.object_list', students),
)
