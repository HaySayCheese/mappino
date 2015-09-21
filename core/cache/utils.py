# coding=utf-8
import mmh3
import os

from django.conf import settings
from django.core.cache import caches



templates_etags_cache = caches['templates_etags']


def generate_template_etag(template_path):
    """
    Returns lambda that generates etag for template "template_name".
    Lambda is returned to make this method compatible with standard django's etag() decorator.

    Etag will be generated only once per server start.
    To drop templates caches server should be simple reloaded.

    :param template_path: path of the template from the templates dir.
    """
    if settings.DEBUG:
        return lambda x: None


    cached_etag = templates_etags_cache.get(template_path)
    if cached_etag:
        return cached_etag

    else:
        file_path = os.path.join(settings.BASE_DIR, 'templates', template_path)
        with open(file_path) as f:
            content = ''.join(f.readlines())
            etag = str(mmh3.hash(content))
            templates_etags_cache.set(template_path, etag)

            return lambda x: etag