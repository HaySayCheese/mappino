# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    # templates
    url(r'', include('apps.common.templates.urls')),

    # api
    url(r'', include('apps.common.api.accounts.urls')),
    url(r'', include('apps.common.api.settings.urls')),
)