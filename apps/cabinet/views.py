from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def main(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/map/#!/account/login')

	template = templates.get_template('cabinet/cabinet.html')
	return HttpResponse(content=template.render())