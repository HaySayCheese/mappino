# coding=utf-8
from apps.cabinet.api.moderators.ban.ajax import AddSuspiciousUser, BanUser
from django.conf.urls import patterns, url


urlpatterns = patterns('',
   # ban user
   url(r'^ajax/api/moderators/ban/add_suspicious_user/$', AddSuspiciousUser.as_view()),
   url(r'^ajax/api/moderators/ban/ban_user/$', BanUser.as_view()),

)
