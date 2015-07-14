# coding=utf-8
from apps.cabinet.api.settings.ajax import AccountView, AvatarUpdate
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/account/$', AccountView.as_view()),
    url(r'^ajax/api/cabinet/account/photo/$', AvatarUpdate.as_view()),
)