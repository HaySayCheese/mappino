# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps.admin',

    # templates
    url(r'^admin/$', 'templates.admin', name='admin'),
    url(r'^admin/login/$', 'templates.login', name='admin/login'),
)
