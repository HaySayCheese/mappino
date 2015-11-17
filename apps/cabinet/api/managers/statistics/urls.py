# coding=utf-8
from apps.cabinet.api.managers.statistics.ajax import PublicationsCount
from django.conf.urls import patterns, url


urlpatterns = patterns('',
   # get all users
   url(r'^ajax/api/managers/statistics/$', PublicationsCount.as_view()),

)
