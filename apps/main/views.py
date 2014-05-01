from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates


@ensure_csrf_cookie
def home(request):
	template = templates.get_template('main/home.html')
	return HttpResponse(content=template.render())