# coding=utf-8
from django.conf.urls import patterns, url

from apps.common.api.settings.ajax import AccountView, AvatarUpdate


urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/account/$', AccountView.as_view()),
    url(r'^ajax/api/cabinet/account/photo/$', AvatarUpdate.as_view()),
)