# -*- coding: utf-8 -*-
from datetime import date

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from people.models import Article, Human, Course, Person, Grant


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
<<<<<<< Updated upstream
    context = {
        'human': get_object_or_404(Human, nickname=nick),
        'papers': get_list_or_404(Article, author__person__human=human),
    }
    return render_to_response('people_paper_list.html', context, RequestContext(request))

=======
    human = Human.objects.filter(nickname=nick)[0]
    papers_article = Article.objects.filter(author=human).filter(type='Article')
    papers_proceeding = Article.objects.filter(author=human).filter(type='Proceeding')
    return render_to_response('people_paper_list.html', locals(), context_instance=RequestContext(request))
>>>>>>> Stashed changes

def people_course(request, nick):
    context = {
        'human': get_object_or_404(Human, nickname=nick),
        'course': get_list_or_404(Course, lectors__human=human),
    }
    return render_to_response('people_course_list.html', context, RequestContext(request))


def people_students(request, nick):
    context = {
        'human': get_object_or_404(Human, nickname=nick),
        'student': get_list_or_404(Person, advisor__human=human),
    }
    return render_to_response('people_student_list.html', context, RequestContext(request))


def people_grants(request, nick):
    context = {
        'human': get_object_or_404(Human, nickname=nick),
        'grants': get_list_or_404(Grant, author__human=human),
    }
    return render_to_response('people_grant_list.html', context, RequestContext(request))
