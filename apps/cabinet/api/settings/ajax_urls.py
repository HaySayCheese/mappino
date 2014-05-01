from django.conf.urls import patterns, url
from core.users.ajax.cabinet import Account


urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/settings/$', Account.as_view()),
)