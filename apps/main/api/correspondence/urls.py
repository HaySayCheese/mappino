#coding=utf-8
from django.conf.urls import patterns, url

from apps.main.api.correspondence.ajax import SendMessageFromClient, SendCallRequestFromClient


urlpatterns = patterns('',
    url(r'^ajax/api/notifications/send-message/(\d+:\w+)/$', SendMessageFromClient.as_view()),
    url(r'^ajax/api/notifications/send-call-request/(\d+:\w+)/$', SendCallRequestFromClient.as_view()),
)