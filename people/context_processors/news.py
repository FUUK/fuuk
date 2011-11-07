def news_list(request):
    from people.models import News
    from datetime import date
    return {'news_list': News.objects.filter(start__lte=date.today(), end__gte=date.today())}