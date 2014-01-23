from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates



#-- templates
@ensure_csrf_cookie
def publications_template(request):
	t =  templates.get_template('cabinet/parts/publications.html')
	return HttpResponse(content=t.render())