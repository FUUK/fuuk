from django.conf.urls import patterns, url, include
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Course, Grant, Thesis

from .views import (ArticleList, Papers, GrantList, ThesisList, PeopleList, PersonDetail, PersonArticles,
                    PersonCourses, PersonStudents, PersonGrants, StudentList, RetiredList)


DOWNLOADS_VIEW = ListView.as_view(queryset=Course.objects.exclude(attachment__isnull=True),
                                  template_name='people/download_list.html')


urlpatterns = patterns('',
    # Global pages
    url(r'^articles/$', ArticleList.as_view(), name="articles"),
    url(r'^articles/(?P<year>[0-9]{4})/$', ArticleList.as_view(), name="articles"),
    url(r'^papers/$', Papers.as_view()),
    # TODO: grants by years
    url(r'^grants/$', GrantList.as_view(), name="grants"),
    url(r'^grants/(?P<pk>\d+)/$', DetailView.as_view(model=Grant), name="grants"),
    url(r'^theses/$', ThesisList.as_view(), name="theses"),
    url(r'^thesis/id=(?P<pk>\d+)/$', DetailView.as_view(model=Thesis), name="theses_detail"),
    url(r'^courses/$', ListView.as_view(model=Course), name="courses"),
    url(r'^downloads/$', DOWNLOADS_VIEW, name="downloads"),
    # Staff menu
    url(r'^phd/$', PeopleList.as_view(), name="phd_list"),
    url(r'^staff/$', PeopleList.as_view(people_type='STAFF', title='Staff'), name="staff_list"),
    url(r'^other/$', PeopleList.as_view(people_type='OTHER', title='Other workers'), name="other_list"),
    url(r'^students/$', StudentList.as_view(), name="student_list"),
    url(r'^graduates/$', PeopleList.as_view(people_type='GRAD', title='Graduate students'), name="graduate_list"),
    url(r'^retired/$', RetiredList.as_view(), name="retired_list"),
)

human_patterns = patterns('',
    # Human details
    url(r'^(?P<slug>\w+)/$', PersonDetail.as_view(), name="person_detail"),
    url(r'^(?P<slug>\w+)/papers/$', PersonArticles.as_view(), name="person_articles"),
    url(r'^(?P<slug>\w+)/papers/first/$', PersonArticles.as_view(first=True), name="person_articles_first"),
    url(r'^(?P<slug>\w+)/courses/$', PersonCourses.as_view(), name="person_courses"),
    url(r'^(?P<slug>\w+)/students/$', PersonStudents.as_view(), name="person_students"),
    url(r'^(?P<slug>\w+)/grants/$', PersonGrants.as_view(), name="person_grants"),
)

urlpatterns = patterns('',
    url(r'^people/', include(urlpatterns)),
    url(r'^', include(human_patterns))
)
