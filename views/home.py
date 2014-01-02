from django.http.response import HttpResponse
from mappino.wsgi import templates


def home(request):
	template = templates.get_template('main/home.html')
	return HttpResponse(content=template.render())