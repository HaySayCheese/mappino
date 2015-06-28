#coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.main.templates',
    url(r'^ajax/template/map/navbar/$', 'navbar'),
    url(r'^ajax/template/map/navbar/tabs/account/$', 'navbar_account'),
    url(r'^ajax/template/map/navbar/tabs/favorites/$', 'navbar_favorites'),
    url(r'^ajax/template/map/navbar/tabs/filters-red/$', 'navbar_filters_red'),
    url(r'^ajax/template/map/navbar/tabs/filters-blue/$', 'navbar_filters_blue'),
    url(r'^ajax/template/map/navbar/tabs/search/$', 'navbar_search'),


    url(r'^ajax/template/map/publication/view/$', 'publication_view'),
    url(r'^ajax/template/map/publication/list/$', 'publication_view_list'),


    # # homepage
    # url(r'^ajax/template/main/home/suggests/$', 'home.suggests_template'),
    # url(r'^ajax/template/main/home/types/$', 'home.types_template'),
    #
    #
    # # login, registration and access restore templates
    # url(r'^ajax/template/main/accounts/login/$', 'accounts.login_template'),
    # url(r'^ajax/template/main/accounts/registration/$', 'accounts.registration_template'),
    # url(r'^ajax/template/main/accounts/access-restore/$', 'accounts.access_restore_template'),
    #
    #
    # # sidebar templates
    # url(r'^ajax/template/main/sidebar/common/$', 'sidebars.common_sidebar_template'),
    # url(r'^ajax/template/main/sidebar/realtors/$', 'sidebars.realtors_sidebar_template'),
    #
    #
    # # publications search engine templates
    # url(r'^ajax/template/main/detailed-dialog/$', 'publications_search.detailed_dlg_template'),
    # url(r'^ajax/template/main/search/$', 'publications_search.search_template'),
    # url(r'^ajax/template/main/first-enter/$', 'publications_search.first_enter_template'),

)

urlpatterns += patterns('apps.main.templates_ajax',
    url(r'^ajax/template/map/filters/(\w+)/(\d+)/$', 'publications_search.filters_form_template'),
)