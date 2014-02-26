from django.conf.urls import patterns, url


#-- angular templates for main pages
urlpatterns = patterns('apps.pages.main',
    url(r'^ajax/template/main/first-enter/$', 'templates_ajax.first_enter_template'),
    url(r'^ajax/template/main/search/$', 'templates_ajax.search_template'),
    url(r'^ajax/template/main/detailed/$', 'templates_ajax.search_template'),

    # filters
    url(r'^ajax/template/main/filters/(\d+)/$', 'templates_ajax.filter_form_template'),
)

#-- angular templates for accounts
urlpatterns += patterns('apps.accounts',
    url(r'^ajax/template/main/accounts/login/$', 'templates_ajax.login_template'),
    url(r'^ajax/template/main/accounts/registration/$', 'templates_ajax.registration_template'),
    url(r'^ajax/template/main/accounts/access-restore/$', 'templates_ajax.access_restore_template'),
)

#-- angular templates for cabinet pages
urlpatterns += patterns('apps.pages.cabinet',
    url(r'^ajax/template/cabinet/publications/$', 'templates_ajax.publications_template'),
)

#-- angular templates publications
urlpatterns += patterns('apps.pages.cabinet',
	# unpublished
    url(r'^ajax/template/cabinet/publications/(\d+)/$', 'templates_ajax.publication_form_template'),
    url(r'^ajax/template/cabinet/publications/map/$', 'templates_ajax.map_template'),
    url(r'^ajax/template/cabinet/publications/photos/$', 'templates_ajax.photos_template'),

	# published
    url(r'^ajax/template/cabinet/published/(\d+)/$', 'templates_ajax.published_publication_form_template'),
)



#-- angular API for main pages
urlpatterns += patterns('apps',
    # login and registration
	url(r'^ajax/api/accounts/registration/$', 'accounts.accounts_ajax.registration_handler'),
    url(r'^ajax/api/accounts/registration/cancel/$', 'accounts.accounts_ajax.registration_cancel_handler'),
    url(r'^ajax/api/accounts/registration/resend-sms/$', 'accounts.accounts_ajax.resend_sms_handler'),
	url(r'^ajax/api/accounts/login/$', 'accounts.accounts_ajax.login_handler'),
	url(r'^ajax/api/accounts/logout/$', 'accounts.accounts_ajax.logout_handler'),
	url(r'^ajax/api/accounts/password-reset/$', 'accounts.accounts_ajax.password_reset_handler'),
    url(r'^ajax/api/accounts/password-reset/check/$', 'accounts.accounts_ajax.check_token_handler'),

        # validators
	    url(r'^ajax/api/accounts/validate-email/$', 'accounts.accounts_ajax.validate_email_handler'),
	    url(r'^ajax/api/accounts/validate-phone-number/$', 'accounts.accounts_ajax.validate_phone_handler'),

		# data getters
        url(r'^ajax/api/accounts/on-login-info/$', 'accounts.accounts_ajax.on_login_info_handler'),


    # markers
    url(r'^ajax/api/markers/$', 'pages.main.markers.ajax.get_markers'),
)

#-- angular API for cabinet
urlpatterns += patterns('apps.pages.cabinet',
    # dirtags
	url(r'^ajax/api/cabinet/dirtags/$', 'dirtags.ajax.dirtags_handler'),
    url(r'^ajax/api/cabinet/dirtags/(\d+)/$', 'dirtags.ajax.dirtags_handler'),
    url(r'^ajax/api/cabinet/dirtags/(\d+)/add-publication/(\d+:\d+)$', 'dirtags.ajax.dirtags_handler'),


    # publications
    url(r'^ajax/api/cabinet/publications/counters/$', 'briefs.ajax.get_counters'),
    url(r'^ajax/api/cabinet/publications/briefs/all/$',
        'briefs.ajax.get', {'section': 'all'}),
    url(r'^ajax/api/cabinet/publications/briefs/published/$',
        'briefs.ajax.get', {'section': 'published'}),
    url(r'^ajax/api/cabinet/publications/briefs/unpublished/$',
        'briefs.ajax.get', {'section': 'unpublished'}),
    url(r'^ajax/api/cabinet/publications/briefs/deleted/$',
        'briefs.ajax.get', {'section': 'deleted'}),
    url(r'^ajax/api/cabinet/publications/briefs/(\d+)/$',
        'briefs.ajax.get', {'section': 'tag'}),

	url(r'^ajax/api/cabinet/publications/$', 'publications.ajax.create'),
	url(r'^ajax/api/cabinet/publications/(\d+:\d+)/$', 'publications.ajax.rud_switch'),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/publish/$', 'publications.ajax.publish'),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/unpublish/$', 'publications.ajax.unpublish'),

    # photos
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/$', 'publications.photos_ajax.upload'),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/(\d+)/$', 'publications.photos_ajax.rud_switch'),


    # search
	url(r'^ajax/api/cabinet/search/$', 'search.ajax.search'),
)



#-- main pages
urlpatterns += patterns('apps.pages.main',
    url(r'^$', 'home.home'),
)

#-- cabinet pages
urlpatterns += patterns('apps.pages.cabinet',
    url(r'^cabinet/$', 'cabinet.cabinet'),
)

