# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps',
    # common
        # accounts API
        url(r'', include('apps.common.api.accounts.urls')),


    # main
    url(r'', include('apps.main.urls')),

    # cabinet
    url(r'', include('apps.cabinet.urls')),


    # core
        # API # todo: move it to the apps
        url(r'', include('core.escaped_fragments_manager.urls')),
)