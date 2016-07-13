from urlparse import urljoin

from django.conf import settings
from django.contrib.flatpages.views import render_flatpage
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import RegexURLResolver
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from fuuk.people.models import Person
from fuuk.people.urls import HUMAN_PATTERNS

from .models import FlatPage


def flatpage(request, url):
    """
    Copy of a `flatpage` view from `django.contrib.flatpages`. Use our `FlatPage` model instead of django one.
    """
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(FlatPage, url=url, sites=site_id)
    except Http404:
        try:
            if not url.endswith('/') and settings.APPEND_SLASH:
                url += '/'
                f = get_object_or_404(FlatPage, url=url, sites=site_id)
                return HttpResponsePermanentRedirect('%s/' % request.path)
            else:
                raise
        except Http404:
            # XXX: Temporary redirection of the old person URLs to the new URLs
            resolver = RegexURLResolver(r'^/', HUMAN_PATTERNS)
            match = resolver.resolve(url)
            if Person.objects.filter(is_active=True, human__nickname=match.kwargs['slug']).exists():
                return HttpResponsePermanentRedirect(urljoin('/people/person/', url[1:]))
            raise
    return render_flatpage(request, f)
