# coding=utf-8
from django.conf.urls import patterns, url
from apps.cabinet.api.moderators.publications.ajax import NextPublicationView, PublicationAcceptOrRejectView


urlpatterns = patterns('',
    url(r'^ajax/api/moderators/publications/next/$', NextPublicationView.as_view()),
    url(r'^ajax/api/moderators/publications/(accept|reject)/$', PublicationAcceptOrRejectView.as_view()),
)