# -*- coding: utf-8 -*-
from datetime import date

from django.db.models import Count
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.db.models import Q

from people.models import Article, Human, Course, Person, Grant, Thesis


def article_list(request, year=None):
    queryset = Article.objects
    if year is not None:
        year = int(year)
        queryset = queryset.filter(year=year)
    queryset = queryset.order_by('-year', '-pk')

    context = {
        'year': year,
        'years': Article.objects.values_list('year', flat=True).annotate(Count('year')).order_by('-year'),
    }
    return object_list(
        request,
        queryset,
        template_name='people/articles.html',
        paginate_by=10,
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
        queryset = queryset.filter(year=int(year))
    if type:
        queryset = queryset.filter(type=type.upper())

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
        'bachelors': Person.objects.filter(type='BC', is_active=True).order_by('last_name')
    }
    return object_list(
        request,
        queryset,
        template_name='people/students.html',
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
        'articles': Article.objects.filter(author__person__human=person.human, type='ARTICLE').order_by('-year'),
        'courses': Course.objects.filter(lectors__human=person.human),
        'students': Person.objects.filter(advisor__human=person.human, is_active=True),
        'grants': Grant.objects.filter(pk__in =
            Grant.objects.filter(author__human=person.human, end__gte=date.today().year).values_list('pk', flat=True)
            | Grant.objects.filter(co_authors__human=person.human, end__gte=date.today().year).values_list('pk', flat=True)
        ).order_by('-end', '-pk'),
    }
    return context


def person_detail(request, nickname):
    context = get_common_context(nickname)
    return render_to_response('people/person/detail.html', context, RequestContext(request))


def person_articles(request, nickname):
    context = get_common_context(nickname)
    if not context['articles']:
        raise Http404

    context['presentations'] = Article.objects.filter(author__person__human=context['person'].human, type__in = ['POSTER', 'TALK']).order_by('-year')
    context['books'] = Article.objects.filter(author__person__human=context['person'].human, type='BOOK').order_by('-year')

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
    if not context['grants']:
        raise Http404

    context['grants_finished'] = Grant.objects.filter(pk__in =
            Grant.objects.filter(author__human=context['person'].human, end__gte=(date.today().year - 2), end__lt=date.today().year).values_list('pk', flat=True) | 
            Grant.objects.filter(co_authors__human=context['person'].human, end__gte=(date.today().year - 2), end__lt=date.today().year).values_list('pk', flat=True)
        ).order_by('-end', '-pk')

    return render_to_response('people/person/grants.html', context, RequestContext(request))
