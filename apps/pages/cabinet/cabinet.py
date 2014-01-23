from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates


@ensure_csrf_cookie
def cabinet(request):
	template = templates.get_template('cabinet/cabinet.html')
	return HttpResponse(content=template.render())