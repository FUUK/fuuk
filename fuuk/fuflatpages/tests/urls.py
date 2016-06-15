from django.conf.urls import include, url

# special urls for flatpage test cases
urlpatterns = [
    url(r'^flatpage_root', include('fuuk.fuflatpages.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
