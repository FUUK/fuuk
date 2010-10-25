# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from people.models import Article, Human
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
