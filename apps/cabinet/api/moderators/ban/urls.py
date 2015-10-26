# coding=utf-8
from apps.cabinet.api.moderators.ban.ajax import AddSuspiciousUser, BanUser, RemoveSuspiciousUser
from django.conf.urls import patterns, url


urlpatterns = patterns('',
   # ban user
   url(r'^ajax/api/moderators/ban/add-suspicious-user/$', AddSuspiciousUser.as_view()),
   url(r'^ajax/api/moderators/ban/remove-suspicious-user/$', RemoveSuspiciousUser.as_view()),
   url(r'^ajax/api/moderators/ban/ban-user/$', BanUser.as_view()),

)
