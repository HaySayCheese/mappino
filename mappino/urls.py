from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps',
    # templates
    url(r'', include('apps.main.templates_ajax.ajax_urls')),
    url(r'', include('apps.cabinet.templates_ajax.ajax_urls')),


    # API for main pages
    url(r'', include('apps.main.api.accounts.urls')),
    url(r'', include('apps.main.api.ajax_urls')),


    # API for cabinet
    url(r'', include('apps.cabinet.api.dirtags.ajax_urls')),
    url(r'', include('apps.cabinet.api.publications.ajax_urls')),
    url(r'', include('apps.cabinet.api.stats.ajax_urls')),
    url(r'', include('apps.cabinet.api.search.ajax_urls')),
    url(r'', include('apps.cabinet.api.support.ajax_urls')),
    url(r'', include('apps.cabinet.api.billing.ajax_urls')),
    url(r'', include('apps.cabinet.api.settings.ajax_urls')),


    # flat pages
    url(r'^$', 'main.views.homepage'),
    url(r'^map/$', 'main.views.map'),

    url(r'^offer/$', 'main.views.offer'),
    url(r'^offer/realtors/$', 'main.views.offer_for_realtors'),
    # url(r'^offer/agencies/$', 'main.views.offer_for_agencies'), # todo


    url(r'^cabinet/$', 'cabinet.views.main'),


    # core ulrs
    url(r'', include('core.escaped_fragments_manager.urls')),
)
