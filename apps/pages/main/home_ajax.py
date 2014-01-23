from django.http.response import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates



#templates
@ensure_csrf_cookie
def first_enter_template(request):
	t = templates.get_template('main/parts/home/first_enter.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def search_template(request):
	t = templates.get_template('main/parts/home/search.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def detailed_templates(request):
	t = templates.get_template('main/parts/home/detailed.html')
	return HttpResponse(content=t.render())