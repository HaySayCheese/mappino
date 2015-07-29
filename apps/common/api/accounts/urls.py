# coding=utf-8
from django.conf.urls import patterns, url
from apps.common.api.accounts.ajax import LoginManager


urlpatterns = patterns('',
    url(r'^ajax/api/accounts/login/$', LoginManager.FirstStep.as_view()),
    url(r'^ajax/api/accounts/login/check-code/$', LoginManager.SecondStep.as_view()),
    url(r'^ajax/api/accounts/on-login-info/$', LoginManager.OnLoginInfo.as_view()),
    url(r'^ajax/api/accounts/logout/$', LoginManager.Logout.as_view()),
)