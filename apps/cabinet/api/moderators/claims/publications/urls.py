# coding=utf-8
from django.conf.urls import patterns, url
from apps.cabinet.api.moderators.claims.publications.ajax import PublicationsClaimsView


urlpatterns = patterns('',
    url(r'^ajax/api/moderators/claims/publications/(opened|archived)/$', PublicationsClaimsView.as_view()),
)