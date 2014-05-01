from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates


@ensure_csrf_cookie
def main(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/#!/account/login')

	template = templates.get_template('cabinet/cabinet.html')
	return HttpResponse(content=template.render())