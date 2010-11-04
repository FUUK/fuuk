# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from people.models import Article, Human, Author, Course, Person, Grant
from datetime import date

def article_list(request, prefix=None):

    if prefix is not None:
        articles = Article.objects.filter(year__icontains=prefix)
    else:
        articles = Article.objects.filter(year__gte=(date.today().year - 1)).order_by('year').reverse()

    years = Article.objects.values_list('year', flat=True).distinct()
    return render_to_response('article_list.html', locals(), context_instance=RequestContext(request))

def people_detail(request, nick):
    try:
        human = Human.objects.filter(nickname=nick)[0]
    except IndexError:
        return HttpResponseRedirect('/people/staff/')    
    return render_to_response('people_detail_list.html', locals(), context_instance=RequestContext(request))

def people_paper(request, nick):
    human = Human.objects.filter(nickname=nick)[0]
    papers = Article.objects.filter(author=human)
    return render_to_response('people_paper_list.html', locals(), context_instance=RequestContext(request))

def people_course(request, nick):
    human = Human.objects.filter(nickname=nick)[0]
    course = Course.objects.filter(lectors=human)
    return render_to_response('people_course_list.html', locals(), context_instance=RequestContext(request))

def people_students(request, nick):
    human = Human.objects.filter(nickname=nick)[0]
    student = Person.objects.filter(advisor=human)
    return render_to_response('people_student_list.html', locals(), context_instance=RequestContext(request))

def people_grants(request, nick):
    human = Human.objects.filter(nickname=nick)[0]
    grants = Grant.objects.filter(author=human)
    return render_to_response('people_grant_list.html', locals(), context_instance=RequestContext(request))
