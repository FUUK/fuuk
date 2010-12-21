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

def grant_detail(request, odkaz):
    queryset = Grant.objects.filter(id=odkaz)
    return object_list(
        request,
        queryset,
        template_name='people/grants_detail.html',
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


def get_person_or_404(nickname):
    try:
        return Person.objects.filter(human__nickname=nickname).order_by('pk')[0]
    except (Person.DoesNotExist, IndexError):
        # (nickname is invalid, no person exist)
        raise Http404


def person_detail(request, nickname):
    context = {
        'person': get_person_or_404(nickname)
    }
    return render_to_response('people/person/detail.html', context, RequestContext(request))


def person_articles(request, nickname):
    person = get_person_or_404(nickname)
    context = {
        'person': person,
        'papers_article': Article.objects.filter(author__person__human=person.human, type='ARTICLE').order_by('-year'),
        'papers_presentation': Article.objects.filter(Q(author__person__human=person.human, type='POSTER') | Q(author__person__human=person.human, type='TALK')).order_by('-year'),
        'papers_book': Article.objects.filter(author__person__human=person.human, type='BOOK').order_by('-year'),
    }
    return render_to_response('people/person/articles.html', context, RequestContext(request))


def person_courses(request, nickname):
    person = get_person_or_404(nickname)
    context = {
        'person': person,
        'courses': get_list_or_404(Course, lectors__human=person.human),
    }
    return render_to_response('people/person/courses.html', context, RequestContext(request))


def person_students(request, nickname):
    person = get_person_or_404(nickname)
    context = {
        'person': person,
        'students': get_list_or_404(Person, advisor__human=person.human, is_active=True),
    }
    return render_to_response('people/person/students.html', context, RequestContext(request))


def person_grants(request, nickname):
    person = get_person_or_404(nickname)
    context = {
        'person': person,
        'grants': Grant.objects.filter(pk__in =
            Grant.objects.filter(author__human=person.human, end__gte=date.today().year).values_list('pk', flat=True) | 
            Grant.objects.filter(co_authors__human=person.human, end__gte=date.today().year).values_list('pk', flat=True)
        ).order_by('-end', '-pk'),
        'grants_finished': Grant.objects.filter(pk__in =
            Grant.objects.filter(author__human=person.human, end__gte=(date.today().year - 2), end__lt=date.today().year).values_list('pk', flat=True) | 
            Grant.objects.filter(co_authors__human=person.human, end__gte=(date.today().year - 2), end__lt=date.today().year).values_list('pk', flat=True)
        ).order_by('-end', '-pk'), 
    }
    return render_to_response('people/person/grants.html', context, RequestContext(request))

def thesis_defend(request):
    context = {
        'types': Thesis.objects.filter(defended=True).values_list('type', flat=True).annotate(Count('type')).order_by('-type'),
        'years': Thesis.objects.filter(defended=True).values_list('year', flat=True).annotate(Count('year')).order_by('-year'),
    }
    return render_to_response('people/thesis_defend_page.html', context, RequestContext(request))

def thesis_defend_ext(request, ext):
    ext = int(ext)
    context = {
        'ext': ext,
        'thesis': Thesis.objects.filter(defended=True, year=ext),
    }
    return render_to_response('people/thesis_defend_ext_page.html', context, RequestContext(request))

def thesis_detail(request, ids):
    ids = int(ids)
    context = {
    'ids': ids,
    'thesis': get_object_or_404(Thesis, id=ids),
    }
    return render_to_response('people/thesis_detail.html', context, RequestContext(request))
