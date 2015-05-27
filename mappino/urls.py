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
        url(r'', include('apps.main.templates_ajax.ajax_urls')),

        # API
        url(r'', include('apps.main.api.ajax_urls')),


    # cabinet
        # flatpages
        url(r'^cabinet/$', 'cabinet.views.main'),
        url(r'^cabinet/login/$', 'cabinet.views.login'),

        # templates
        url(r'', include('apps.cabinet.templates.ajax_urls')),

        # API
        url(r'', include('apps.cabinet.api.dirtags.ajax_urls')),
        url(r'', include('apps.cabinet.api.publications.ajax_urls')),
        url(r'', include('apps.cabinet.api.stats.ajax_urls')),
        url(r'', include('apps.cabinet.api.search.ajax_urls')),
        url(r'', include('apps.cabinet.api.support.ajax_urls')),
        url(r'', include('apps.cabinet.api.billing.ajax_urls')),
        url(r'', include('apps.cabinet.api.settings.ajax_urls')),


    # core
        # API
        url(r'', include('core.escaped_fragments_manager.urls')),
)
