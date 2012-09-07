from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('',
    # Global pages
    url(r'^articles/$', 'people.views.article_list', name="articles"),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list', name="articles"),
    url(r'^papers/$', 'people.views.papers'),
    # TODO: grants by years
    url(r'^grants/$', 'people.views.grant_list', name="grants"),
    url(r'^grants/(\d+)/$', 'people.views.grant_detail', name="grants"),
    url(r'^theses/$', 'people.views.thesis_list', name="theses"),
    url(r'^thesis/id=(\d+)/$', 'people.views.thesis_detail'),
    url(r'^courses/$', 'people.views.course_list', name="courses"),
    url(r'^downloads/$', 'people.views.download_list', name="downloads"),

    # Staff menu
    url(r'^phd/$', 'people.views.phd_list', name="phd_list"),
    url(r'^staff/$', 'people.views.staff_list', name="staff_list"),
    url(r'^other/$', 'people.views.other_list', name="other_list"),
    url(r'^students/$', 'people.views.student_list', name="student_list"),
    url(r'^graduates/$', 'people.views.graduate_list', name="graduate_list"),
    url(r'^retired/$', 'people.views.retired_list', name="retired_list"),
)

human_patterns = patterns('',
    # Human details
    url(r'^(\w+)/$', 'people.views.person_detail', name="person_detail"),
    url(r'^(\w+)/papers/$', 'people.views.person_articles', name="person_articles"),
    url(r'^(\w+)/courses/$', 'people.views.person_courses', name="person_courses"),
    url(r'^(\w+)/students/$', 'people.views.person_students', name="person_students"),
    url(r'^(\w+)/grants/$', 'people.views.person_grants', name="person_grants"),
)

urlpatterns = patterns('',
    url(r'^people/', include(urlpatterns)),
    url(r'^', include(human_patterns))
)