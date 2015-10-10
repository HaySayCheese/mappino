# coding=utf-8
from django.conf.urls import patterns, url

from apps.main.api.publications_and_markers.ajax import Markers, DetailedView


urlpatterns = patterns('',
   url(r'^ajax/api/markers/$', Markers.as_view()),

   url(r'^ajax/api/detailed/publication/(\d+):(\w+)/$', DetailedView.as_view()),
)
