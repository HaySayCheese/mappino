#coding=utf-8
from django.conf.urls import patterns, url

from apps.main.api.contacts.ajax import Contacts


urlpatterns = patterns('',
    url(r'^ajax/api/detailed/publication/(\d+):(\w+)/contacts/$', Contacts.as_view()),
)