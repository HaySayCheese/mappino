from django.conf.urls import patterns, include, url


#-- angular templates for main pages
urlpatterns = patterns('apps.pages.main',
    url(r'^ajax/template/main/first-enter/$', 'home_ajax.first_enter_template'),
    url(r'^ajax/template/main/search/$', 'home_ajax.search_template'),
    url(r'^ajax/template/main/detailed/$', 'home_ajax.search_template'),
)

#-- angular templates for accounts
urlpatterns += patterns('apps.accounts',
    url(r'^ajax/template/main/accounts/login/$', 'accounts_ajax.login_template'),
    url(r'^ajax/template/main/accounts/registration/$', 'accounts_ajax.registration_template'),
)

#-- angular templates for cabinet pages
urlpatterns += patterns('apps.pages.main',
    # ...
)



#-- angular API for main pages
urlpatterns += patterns('apps',
    # login and registration
	url(r'^ajax/api/accounts/registration/$', 'accounts.accounts_ajax.registration_handler'),
	url(r'^ajax/api/accounts/login/$', 'accounts.accounts_ajax.login_handler'),

        # validators
	    url(r'^ajax/api/accounts/validate-email/$', 'accounts.accounts_ajax.validate_email_handler'),
	    url(r'^ajax/api/accounts/validate-phone-number/$', 'accounts.accounts_ajax.validate_phone_handler'),


)



#-- main pages
urlpatterns += patterns('apps.pages.main',
    url(r'^$', 'home.home'),
)

#-- cabinet pages
urlpatterns += patterns('apps.pages.cabinet',
    url(r'^cabinet/$', 'cabinet.cabinet'),
)

