from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates



@ensure_csrf_cookie
def home(request):
    template = templates.get_template('main/home.html')
    return HttpResponse(content=template.render())



def offer(request):
    return HttpResponseRedirect('/offer/realtors/')



def offer_for_realtors(request):
    template = templates.get_template('main/offer/realtors.html')
    return HttpResponse(content=template.render())



def offer_for_agencies(request):
    template = templates.get_template('main/offer/agencies.html')
    return HttpResponse(content=template.render())