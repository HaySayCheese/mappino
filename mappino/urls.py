# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps',
    # common
        # accounts API
        url(r'', include('apps.common.api.accounts.urls')),


    # main
        # flatpages
        url(r'^$', 'main.views.homepage'),
        url(r'^map/$', 'main.views.map'),

        # templates
        url(r'', include('apps.main.templates.urls')),

        # API
        url(r'', include('apps.main.api.ajax_urls')),


    # cabinet
    url(r'', include('apps.cabinet.urls')),


    # core
        # API
        url(r'', include('core.escaped_fragments_manager.urls')),
)