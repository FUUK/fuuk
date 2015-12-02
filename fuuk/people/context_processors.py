from datetime import date

from fuuk.people.models import News


def news_list(request):
    return {'news_list': News.objects.filter(start__lte=date.today(), end__gte=date.today())}
