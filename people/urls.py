# -*- coding: utf-8 -*-
from datetime import date

from django.conf.urls.defaults import patterns, url
from people.models import Person, Grant
from django.utils.translation import ugettext as _

# TODO: move to views
grants = {
    'queryset': Grant.objects.filter(end__gte=date.today().year),
    'template_name': 'grant_list.html',
    'template_object_name': 'grants',
    'extra_context': {
        'grants2_list': Grant.objects.filter(end__gte=(date.today().year - 2), end__lt=date.today().year),
    },
}

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
    # Global pages
    # This might not have to be split in here, try use django generic views
    url(r'^articles/$', 'people.views.article_list', name="article_list"),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list', name="article_list_year"),
    url(r'^grants/$', 'django.views.generic.list_detail.object_list', grants, name="grant_list"),

    # Staff menu
    url(r'^phd/$', 'django.views.generic.list_detail.object_list', phds, name="phd_list"),
    url(r'^staff/$', 'django.views.generic.list_detail.object_list', staff, name="staff_list"),
    url(r'^students/$', 'django.views.generic.list_detail.object_list', students, name="student_list"),

    # Human details
    url(r'^detail/(\w+)/$', 'people.views.people_detail', name="person_detail"),
    url(r'^detail/(\w+)/papers/$', 'people.views.people_paper', name="person_articles"),
    url(r'^detail/(\w+)/courses/$', 'people.views.people_course', name="person_courses"),
    url(r'^detail/(\w+)/students/$', 'people.views.people_students', name="person_students"),
    url(r'^detail/(\w+)/grants/$', 'people.views.people_grants', name="person_grants"),
)
