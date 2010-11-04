# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from people.models import Person
from django.utils.translation import ugettext as _

admin.autodiscover()

phds = {
    'queryset': Person.objects.filter(type__icontains='PHD').order_by('last_name'),
    'template_name': 'people_list.html',
    'template_object_name': 'people',
    'extra_context': {"text": _('PhD. students')},
}

staff = {
    'queryset': Person.objects.filter(type__icontains='STAFF').order_by('last_name'),
    'template_name': 'people_list.html',
    'template_object_name': 'people',
    'extra_context': {"text": _('Staff')},
}

students = {
    'queryset': Person.objects.filter(type__icontains='MGR').order_by('last_name'),
    'template_name': 'student_list.html',
    'template_object_name': 'people',
    'extra_context': {'people2_list': Person.objects.filter(type__icontains='BC').order_by('last_name')},
}

urlpatterns = patterns('',
    url(r'^phd/$', 'django.views.generic.list_detail.object_list', phds),
    url(r'^staff/$', 'django.views.generic.list_detail.object_list', staff),
    url(r'^students/$', 'django.views.generic.list_detail.object_list', students),
    url(r'^detail/(\w+)/$', 'people.views.people_detail'),
    url(r'^detail/(\w+)/papers/$', 'people.views.people_paper'),
    url(r'^detail/(\w+)/courses/$', 'people.views.people_course'),
    url(r'^detail/(\w+)/students/$', 'people.views.people_students'),
    url(r'^detail/(\w+)/grants/$', 'people.views.people_grants'),
)
