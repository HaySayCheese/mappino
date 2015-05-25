# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps.admin',
    # flat pages
    url(r'^admin/$', 'views.admin', name='admin'),
    url(r'^admin/login/$', 'views.login', name='admin/login'),
)
