from django.conf.urls import patterns, include, url


#-- main pages
urlpatterns = patterns('apps.pages.main',
    url(r'^$', 'home.home'),
)

#-- angular templates for main pages
urlpatterns += patterns('apps.pages.main',
    #-- homepage
    url(r'^ajax/template/home/first-enter/$', 'home_ajax.first_enter_template'),
    url(r'^ajax/template/home/search/$', 'home_ajax.search_template'),
)



#-- cabinet pages
urlpatterns += patterns('apps.pages.cabinet',
    url(r'^cabinet/$', 'cabinet.cabinet'),
)

#-- angular templates for cabinet pages
urlpatterns += patterns('apps.pages.main',
    # ...
)