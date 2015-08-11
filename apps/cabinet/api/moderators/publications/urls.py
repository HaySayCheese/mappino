# coding=utf-8
from django.conf.urls import patterns, url
from apps.cabinet.api.moderators.claims.publications.ajax import PublicationView, PublicationAcceptRejectOrHoldView
from apps.cabinet.api.moderators.publications.ajax import \
    NextPublicationView, PublicationAcceptOrRejectView, PublicationMessageView



urlpatterns = patterns('',
    url(r'^ajax/api/moderators/publications/next/$', NextPublicationView.as_view()),
    url(r'^ajax/api/moderators/publications/(\d+):(\w+)/$', PublicationView.as_view()),
    url(r'^ajax/api/moderators/publications/(\d+):(\w+)/(accept|reject|hold)/$', PublicationAcceptRejectOrHoldView.as_view()),
)