# coding=utf-8
from django.conf.urls import patterns, url
from apps.main.api.claims.ajax import ClaimsView


urlpatterns = patterns('',
    url(r'^ajax/api/publications/(\d+):(\w+)/claims/$', ClaimsView.as_view()),
)