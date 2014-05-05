from django.conf.urls import patterns, url
from apps.cabinet.api.settings.ajax import PersonalPagesAliasesManager

from core.users.ajax.cabinet import Account


urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/settings/$', Account.as_view()),

    url(r'^ajax/api/cabinet/settings/personal-page-aliases/validate/$', PersonalPagesAliasesManager.ValidateAlias.as_view()),
    url(r'^ajax/api/cabinet/settings/personal-page-aliases/$', PersonalPagesAliasesManager.SetAlias.as_view()),
)