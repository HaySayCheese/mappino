# coding=utf-8
from apps.cabinet.api.managers.users.ajax import AllUsers, UsersPublications
from django.conf.urls import patterns, url


urlpatterns = patterns('',
   # get all users
   url(r'^ajax/api/managers/users/$', AllUsers.as_view()),
   url(r'^ajax/api/managers/users/(\w+)/publications/$', UsersPublications.as_view()),

)
