from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import condition
from core.cache.templates_cache import static_template_last_modified
from core.utils.jinja2_integration import templates



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def homepage_template(request):
    t = templates.get_template('main/home/home.html')
    return HttpResponse(t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def suggests_template(request):
    t = templates.get_template('main/home/checkboxes/suggests.html')
    return HttpResponse(t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def types_template(request):
    t = templates.get_template('main/home/checkboxes/types.html')
    return HttpResponse(t.render())