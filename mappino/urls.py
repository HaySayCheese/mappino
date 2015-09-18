# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps',
    # common
    url(r'', include('apps.common.urls')),

    # main
    url(r'', include('apps.main.urls')),

    # cabinet
    url(r'', include('apps.cabinet.urls')),

    # todo: move it to the apps
    # # core
    #     # API
    #     url(r'', include('core.escaped_fragments_manager.urls')),
)