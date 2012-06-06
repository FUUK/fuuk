# -*- coding: utf-8 -*-
from datetime import date

from django.core.urlresolvers import reverse  
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list, object_detail

from people.models import Article, Course, Person, Grant, Thesis, News



def article_list(request, year=None):
    queryset = Article.objects.filter(type__in = ('ARTICLE', 'BOOK'))
    if not queryset:
        raise Http404
    
    years = queryset.values_list('year', flat=True).annotate(Count('year')).order_by('-year')
    if year is None:
        year = years[0]
    else:
        year = int(year)
    queryset = queryset.filter(year=year).order_by('-year', '-pk')
    
    if not queryset:
        return HttpResponseRedirect(reverse('articles'))
    
    context = {
        'year': year,
        'years': years,
    }
    return object_list(
        request,
        queryset,
        template_name='people/articles.html',
        paginate_by=50,
        extra_context=context,
    )


def grant_list(request):
    queryset = Grant.objects.filter(end__gte=date.today().year).order_by('-end', '-pk')
    grants_finished = Grant.objects.filter(end__gte=(date.today().year - 2), end__lt=date.today().year).order_by('-end', '-pk')
    context = {
        'grants_finished': grants_finished,
    }
    return object_list(
        request,
        queryset,
        template_name='people/grants.html',
        extra_context=context,
    )


def grant_detail(request, object_id):
    queryset = Grant.objects
    return object_detail(
        request,
        queryset,
        object_id=object_id,
        template_name='people/grant_detail.html',
    )


def thesis_list(request):
    year = request.GET.get('year', None)
    type = request.GET.get('type', None)

    queryset = Thesis.objects.filter(defended=True)
    if year:
        queryset = queryset.filter(year=int(year)).order_by('-type')
    if type:
        queryset = queryset.filter(type=type.upper()).order_by('-year')

    # we got filter but no results
    if (year or type):
        if not queryset:
            raise Http404
    else:
        queryset = queryset.none()

    types = Thesis.objects.filter(defended=True).values_list('type', flat=True).annotate(Count('type')).order_by('-type')

    context = {
        'types': [(type, Thesis(type=type).get_type_display()) for type in types],
        'years': Thesis.objects.filter(defended=True).values_list('year', flat=True).annotate(Count('year')).order_by('-year'),
        'year': year,
        'type': type,
    }
    return object_list(
        request,
        queryset,
        template_name='people/theses.html',
        extra_context=context,
    )


def thesis_detail(request, object_id):
    object_id = int(object_id)
    context = {
        'thesis': get_object_or_404(Thesis, pk=object_id),
    }
    return render_to_response('people/thesis_detail.html', context, RequestContext(request))


def course_list(request):
    queryset = Course.objects.order_by('pk')
    return object_list(
        request,
        queryset,
        template_name='courses.html',
    )


def download_list(request):
    queryset = Course.objects.filter(attachment__isnull=False).order_by('pk')
    return object_list(
        request,
        queryset,
        template_name='downloads.html',
        )

def staff_list(request):
    queryset = Person.objects.filter(type='STAFF', is_active=True).order_by('last_name')
    context = {
        "title": _('Staff')
    }
    return object_list(
        request,
        queryset,
        template_name='people/people.html',
        extra_context=context,
    )
    
    
def other_list(request):
    queryset = Person.objects.filter(type='OTHER', is_active=True).order_by('last_name')
    context = {
        "title": _('Other workers')
    }
    return object_list(
        request,
        queryset,
        template_name='people/people.html',
        extra_context=context,
    )


def phd_list(request):
    queryset = Person.objects.filter(type='PHD', is_active=True).order_by('last_name')
    context = {
        "title": _('PhD. students')
    }
    return object_list(
        request,
        queryset,
        template_name='people/people.html',
        extra_context=context,
    )


def student_list(request):
    queryset = Person.objects.filter(type='MGR', is_active=True).order_by('last_name')
    context = {
        'bachelors': Person.objects.filter(type='BC', is_active=True).order_by('last_name'),
        'students': Person.objects.filter(type='STUDENT', is_active=True).order_by('last_name'),
    }
    return object_list(
        request,
        queryset,
        template_name='people/students.html',
        extra_context=context,
    )


def graduate_list(request):
    queryset = Person.objects.filter(type='GRAD', is_active=True).order_by('last_name')
    context = {
        "title": _('Graduate students')
    }
    return object_list(
        request,
        queryset,
        template_name='people/people.html',
        extra_context=context,
    )


def retired_list(request):
    queryset = Person.objects.filter(type='STAFF', is_active=False).order_by('last_name') | Person.objects.filter(type='OTHER', is_active=False).order_by('last_name')
    context = {
        "title": _('Retired workers')
    }
    return object_list(
        request,
        queryset,
        template_name='people/people.html',
        extra_context=context,
    )
    
### Person pages
def get_common_context(nickname):
    try:
        person = Person.objects.filter(human__nickname=nickname).order_by('pk')[0]
    except (Person.DoesNotExist, IndexError):
        # (nickname is invalid, no person exist)
        raise Http404

    context = {
        'person': person,
        'publications': Article.objects.filter(author__person__human=person.human).order_by('-year'),
        'courses': Course.objects.filter(lectors__human=person.human).order_by('pk'),
        'courses_practical': Course.objects.filter(practical_lectors__human=person.human).order_by('pk'),
        'students': Person.objects.filter(advisor__human=person.human, is_active=True).order_by('last_name', 'first_name'),
        'grants': Grant.objects.filter(pk__in =
            Grant.objects.filter(author__human=person.human, end__gte=date.today().year).values_list('pk', flat=True)
            | Grant.objects.filter(co_authors__human=person.human, end__gte=date.today().year).values_list('pk', flat=True)
        ).order_by('-end', '-pk'),
        'grants_finished': Grant.objects.filter(pk__in =
            Grant.objects.filter(author__human=person.human, end__lt=date.today().year).values_list('pk', flat=True)
            | Grant.objects.filter(co_authors__human=person.human, end__lt=date.today().year).values_list('pk', flat=True)
        ).order_by('-end', '-pk')
    }
    return context


def person_detail(request, nickname):
    context = get_common_context(nickname)
    context['theses'] = Thesis.objects.filter(author__human=context['person'].human, defended=True).order_by('-year')
    context['theses_ongoing'] = Thesis.objects.filter(author__human=context['person'].human, defended=False).order_by('-year')
    return render_to_response('people/person/detail.html', context, RequestContext(request))


def person_articles(request, nickname):
    context = get_common_context(nickname)
    if not context['publications']:
        raise Http404

    if context['person'].human.display_posters:
        presentation_types = ['POSTER', 'TALK', 'INVITED']
    else:
        presentation_types = ['TALK', 'INVITED']
    context['articles'] = context['publications'].filter(type='ARTICLE')
    if context['person'].human.display_talks:
        context['presentations'] = context['publications'].filter(type__in=presentation_types)
    else:
        context['presentations'] = context['publications'].filter(type__in=presentation_types).filter(presenter__human=context['person'].human)
    context['books'] = context['publications'].filter(type='BOOK')

    return render_to_response('people/person/articles.html', context, RequestContext(request))


def person_courses(request, nickname):
    context = get_common_context(nickname)
    if not context['courses']:
        raise Http404

    return render_to_response('people/person/courses.html', context, RequestContext(request))


def person_students(request, nickname):
    context = get_common_context(nickname)
    if not context['students']:
        raise Http404

    return render_to_response('people/person/students.html', context, RequestContext(request))


def person_grants(request, nickname):
    context = get_common_context(nickname)
    if not (context['grants'] or context['grants_finished']):
        raise Http404

    return render_to_response('people/person/grants.html', context, RequestContext(request))
