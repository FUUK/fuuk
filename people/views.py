# -*- coding: utf-8 -*-
from datetime import date
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from people.models import Article, Human, Course, Person, Grant
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

def article_list(request, prefix=None):
    if prefix is not None:
        articles = Article.objects.filter(year__icontains=prefix)
    else:
        articles = Article.objects.filter(year__gte=(date.today().year - 1)).order_by('year').reverse()

    context = {
        'prefix': prefix,
        # TODO: remove distinct :-!
        'years': Article.objects.values_list('year', flat=True).distinct(),
        'articles': articles,
    }
    return render_to_response('article_list.html', context, RequestContext(request))


def people_detail(request, nick):
    context = {
        'human': get_object_or_404(Human, nickname=nick),
    }
    return render_to_response('people_detail_list.html', context, RequestContext(request))


def people_paper(request, nick):
    human = get_object_or_404(Human, nickname=nick)
    context = {
        'human': human,
        'papers_article': Article.objects.filter(author__person__human=human, type='Article'),
        'papers_proceeding': Article.objects.filter(author__person__human=human, type='Proceeding'),
    }
    return render_to_response('people_paper_list.html', context, RequestContext(request))

def people_course(request, nick):
    human = get_object_or_404(Human, nickname=nick)
    context = {
        'human': human,
        'course': get_list_or_404(Course, lectors__human=human),
    }
    return render_to_response('people_course_list.html', context, RequestContext(request))


def people_students(request, nick):
    human = get_object_or_404(Human, nickname=nick)
    context = {
        'human': human,
        'student': get_list_or_404(Person, advisor__human=human),
    }
    return render_to_response('people_student_list.html', context, RequestContext(request))


def people_grants(request, nick):
    human = get_object_or_404(Human, nickname=nick)
    context = {
        'human': human,
        'grants': get_list_or_404(Grant, author__human=human),
    }
    return render_to_response('people_grant_list.html', context, RequestContext(request))

def grant_list(request):
    queryset = Grant.objects.filter(end__gte=date.today().year)   
    context = {
        'template_name': 'grant_list.html',
        'template_object_name': 'grants',
        'extra_context': {
            'grants2_list': Grant.objects.filter(end__gte=(date.today().year - 2), end__lt=date.today().year),
        },   
    }
    return object_list(request, queryset, **context)

def staff_list(request):
    queryset = Person.objects.filter(type='STAFF').order_by('last_name')    
    context = {
        'template_name': 'people_list.html',
        'template_object_name': 'people',
        'extra_context': {
            "text": _('Staff')
        },
    }
    return object_list(request, queryset, **context)

def phd_list(request):
    queryset = Person.objects.filter(type='PHD').order_by('last_name')
    context = {
        'template_name': 'people_list.html',
        'template_object_name': 'people',
        'extra_context': {
            "text": _('PhD. students')
        },
    }
    return object_list(request, queryset, **context)

def student_list(request):
    queryset = Person.objects.filter(type='MGR').order_by('last_name')
    context = {
        'template_name': 'student_list.html',
        'template_object_name': 'people',
        'extra_context': {
            'people2_list': Person.objects.filter(type__icontains='BC').order_by('last_name')
        },
    }
    return object_list(request, queryset, **context)
