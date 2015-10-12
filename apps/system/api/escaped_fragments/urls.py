# coding=utf-8
from apps.system.api.escaped_fragments.ajax import GetPublications
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # list
    url(r'^ajax/api/get_publications/$', GetPublications.as_view()),

)
