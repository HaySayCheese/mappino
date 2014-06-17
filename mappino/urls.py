from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps',
    # templates
    url(r'', include('apps.main.templates_ajax.ajax_urls')),
	url(r'', include('apps.cabinet.templates_ajax.ajax_urls')),


    # API for main pages
    url(r'', include('core.users.ajax_urls')), # registration, login and password reset
    url(r'', include('apps.main.api.ajax_urls')),


    # API for cabinet
    url(r'', include('apps.cabinet.api.dirtags.ajax_urls')),
    url(r'', include('apps.cabinet.api.publications.ajax_urls')),
    url(r'', include('apps.cabinet.api.stats.ajax_urls')),
    url(r'', include('apps.cabinet.api.search.ajax_urls')),
    url(r'', include('apps.cabinet.api.support.ajax_urls')),


    url(r'', include('apps.cabinet.api.accounts.ajax_urls')),


    # flat pages
    url(r'^$', 'main.views.home'),
    url(r'^promo/$', 'main.views.promo'),
    url(r'^cabinet/$', 'cabinet.views.main'),
)
