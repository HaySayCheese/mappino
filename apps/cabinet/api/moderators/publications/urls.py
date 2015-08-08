# coding=utf-8
from django.conf.urls import patterns, url
from apps.cabinet.api.moderators.publications.ajax import NextPublicationView



urlpatterns = patterns('',
    url(r'^ajax/api/moderators/publications/next/$', NextPublicationView.as_view()),
)