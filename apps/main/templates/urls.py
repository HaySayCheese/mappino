#coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.main.templates.templates',
    url(r'^ajax/template/map/navbar-left/$', 'map_navbar_left'),
    url(r'^ajax/template/map/navbar-right/$', 'map_navbar_right'),

    url(r'^ajax/template/map/filters/(\w+)/(\d+)/$', 'filters_form_by_tid'),

    url(r'^ajax/template/map/publication/view/$', 'publication_view'),
    url(r'^ajax/template/map/publication/seller-contacts/$', 'seller_contacts'),
)