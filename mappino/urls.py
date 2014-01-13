from django.conf.urls import patterns, include, url


#-- main pages
urlpatterns = patterns('apps.pages.main',
    url(r'^$', 'home.home'),
)

#-- angular templates for main pages
urlpatterns += patterns('apps.pages.main',
    url(r'^ajax/template/main/first-enter/$', 'home_ajax.first_enter_template'),
    url(r'^ajax/template/main/search/$', 'home_ajax.search_template'),
    url(r'^ajax/template/main/detailed/$', 'home_ajax.search_template'),
    url(r'^ajax/template/main/accounts/login/$', 'accounts_ajax.login_template'),
    url(r'^ajax/template/main/accounts/registration/$', 'accounts_ajax.registration_template'),
)

#-- angular API for main pages
urlpatterns += patterns('apps',
    url(r'^ajax/api/accounts/validate-email/$', 'accounts.accounts_ajax.validate_email_handler'),
)


#-- cabinet pages
urlpatterns += patterns('apps.pages.cabinet',
    url(r'^cabinet/$', 'cabinet.cabinet'),
)

#-- angular templates for cabinet pages
urlpatterns += patterns('apps.pages.main',
    # ...
)