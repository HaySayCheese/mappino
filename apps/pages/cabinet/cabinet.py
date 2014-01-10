from django.http import HttpResponse
from mappino.wsgi import templates


def cabinet(request):
	template = templates.get_template('cabinet/cabinet.html')
	return HttpResponse(content=template.render())