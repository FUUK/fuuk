from django import template

register = template.Library()

def citation(article):
    pages = None
    if article.page_from:
        if article.page_to:
            if article.article_number:
                pages = u"%s (%s" % (article.page_from, article.page_to)
            else:
                pages = u"%s-%s" % (article.page_from, article.page_to)
        else:
            pages = unicode (article.page_from)

    tag_context = {
        'authors': article.author_set.select_related('person').order_by('order'),
        'identification': article.identification,
        'title': article.title,
        'publication': article.publication,
        'volume': article.volume,
        'place': article.place,
        'year': article.year,
        'pages': pages,
        'type': article.type,
        'presenter': article.presenter,
        'type_verbose': article.get_type_display(),
        'editors': article.editors,
        'publishers': article.publishers,
        'article_number': article.article_number,
    }
    return tag_context

register.inclusion_tag('people/citation.html')(citation)
