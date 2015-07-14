# coding=utf-8
from django.http import HttpResponse
from core.utils.jinja2_integration import templates


def render_jinja2_template(f, cache_control=None):
    def wrapper(*args, **kwargs):
        return HttpResponse(
            templates.get_template(f(*args, **kwargs)).render()
        )
    return wrapper