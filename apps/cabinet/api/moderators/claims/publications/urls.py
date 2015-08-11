# coding=utf-8
from django.conf.urls import patterns, url
from apps.cabinet.api.moderators.claims.publications.ajax import PublicationView, NextPublicationToCheckView, \
    PublicationAcceptRejectOrHoldView, ClaimsNoticeView, ClaimCloseView

urlpatterns = patterns('',
    url(r'^ajax/api/moderators/publications/next/$', NextPublicationToCheckView.as_view()),
    url(r'^ajax/api/moderators/publications/(\d+):(\w+)/$', PublicationView.as_view()),
    url(r'^ajax/api/moderators/publications/(\d+):(\w+)/(accept|reject|hold)/$', PublicationAcceptRejectOrHoldView.as_view()),

    url(r'^ajax/api/moderators/claims/(\w+)/notice/$', ClaimsNoticeView.as_view()),
    url(r'^ajax/api/moderators/claims/(\w+)/close/$', ClaimCloseView.as_view()),
)