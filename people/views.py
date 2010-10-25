# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from people.models import Article
from datetime import datetime
from django.db.models import Q

def article_list(request, prefix=None):

    if prefix is not None:
        articles = Article.objects.filter(year__icontains=prefix)
    else:
        articles = Article.objects.filter(Q(year=2010) | Q(year=2009)).order_by('year').reverse()

    years = Article.objects.values_list('year', flat=True).distinct()
    
    return render_to_response('article_list.html', locals(), context_instance=RequestContext(request))
