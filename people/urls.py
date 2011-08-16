from django.conf.urls.defaults import patterns, url, handler404


urlpatterns = patterns('',
    # Global pages
    url(r'^articles/$', 'people.views.article_list', name="articles"),
    url(r'^articles/([0-9]{4})/$', 'people.views.article_list', name="articles"),
    # TODO: grants by years
    url(r'^grants/$', 'people.views.grant_list', name="grants"),
    url(r'^grants/(\d+)/$', 'people.views.grant_detail', name="grants"),
    url(r'^theses/$', 'people.views.thesis_list', name="theses"),
    url(r'^thesis/id=(\d+)/$', 'people.views.thesis_detail'),

    # Staff menu
    url(r'^phd/$', 'people.views.phd_list', name="phd_list"),
    url(r'^staff/$', 'people.views.staff_list', name="staff_list"),
    # TODO: split students to masters and bachelors?
    url(r'^students/$', 'people.views.student_list', name="student_list"),

    # Human details
    url(r'^detail/(\w+)/$', 'people.views.person_detail', name="person_detail"),
    url(r'^detail/(\w+)/papers/$', 'people.views.person_articles', name="person_articles"),
    url(r'^detail/(\w+)/courses/$', 'people.views.person_courses', name="person_courses"),
    url(r'^detail/(\w+)/students/$', 'people.views.person_students', name="person_students"),
    url(r'^detail/(\w+)/grants/$', 'people.views.person_grants', name="person_grants"),
)
