# coding=utf-8
from django.conf.urls import patterns, url

from apps.main.api.correspondence.ajax import ClientNotificationsHandler

urlpatterns = patterns('',
                       url(r'^ajax/api/notifications/send-message/(\d+):(\w+)/$',
                           ClientNotificationsHandler.MessagesHandler.as_view()),
                       url(r'^ajax/api/notifications/send-call-request/(\d+):(\w+)/$',
                           ClientNotificationsHandler.CallRequestsHandler.as_view()),
                       )
