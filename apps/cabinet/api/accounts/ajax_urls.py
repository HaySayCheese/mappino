from apps.cabinet.api.accounts.ajax import AccountManager
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/account/$', AccountManager.AccountView.as_view()),
    url(r'^ajax/api/cabinet/account/photo/$', AccountManager.AvatarUpdate.as_view()),
)