from django.http import HttpResponseServerError
from django.template import loader, RequestContext


def handler500(request):
    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(RequestContext(request)))