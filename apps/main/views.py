from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def home(request):
    template = templates.get_template('main/home.html')
    return HttpResponse(content=template.render())


# @ensure_csrf_cookie
# def search(request):
#     template = templates.get_template('main/home.html')
#     return HttpResponse(content=template.render())


@ensure_csrf_cookie
def promo(request):
    template = templates.get_template('main/promo-pages/promo.html')
    return HttpResponse(content=template.render())


@ensure_csrf_cookie
def realtors_promo(request):
    template = templates.get_template('main/promo-pages/realtors.html')
    return HttpResponse(content=template.render())