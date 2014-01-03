from django.conf.urls import patterns, include, url


#-- pages
urlpatterns = patterns('apps.pages',
    url(r'^$', 'home.home'),
)


#-- angular templates for pages
urlpatterns += patterns('apps.pages',
    #-- homepage
    url(r'^ajax/template/home/first-enter/$', 'home_ajax.first_enter_template'),
    url(r'^ajax/template/home/search/$', 'home_ajax.search_template'),
)
