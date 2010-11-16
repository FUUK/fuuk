# -*- coding: utf-8 -*-
from datetime import date

from django.conf.urls.defaults import patterns, url
from people.models import Person, Grant

urlpatterns = patterns('',
    # Global pages
    url(r'^articles/$', 'people.views.article_list', name="article_list"),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list', name="article_list_year"),
    url(r'^grants/$', 'people.views.grant_list', name="grant_list"),

    # Staff menu
    url(r'^phd/$', 'people.views.phd_list', name="phd_list"),
    url(r'^staff/$', 'people.views.staff_list', name="staff_list"),
    url(r'^students/$', 'people.views.student_list', name="student_list"),

    # Human details
    url(r'^detail/(\w+)/$', 'people.views.people_detail', name="person_detail"),
    url(r'^detail/(\w+)/papers/$', 'people.views.people_paper', name="person_articles"),
    url(r'^detail/(\w+)/courses/$', 'people.views.people_course', name="person_courses"),
    url(r'^detail/(\w+)/students/$', 'people.views.people_students', name="person_students"),
    url(r'^detail/(\w+)/grants/$', 'people.views.people_grants', name="person_grants"),
)
