# coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet',
    # accounts
    url(r'^ajax/template/cabinet/login/$', 'templates.login.login'),


    # briefs
    url(r'^ajax/template/cabinet/publications/briefs/$', 'templates.publications.briefs'),
    url(r'^ajax/template/cabinet/publications/publication/$', 'templates.publications.publication'),


    # unpublished publications forms
    url(r'^ajax/template/cabinet/publications/unpublished/(\d+)/$', 'templates.publications.unpublished_form'),
    url(r'^ajax/template/cabinet/publications/unpublished/map/$', 'templates.publications.unpublished_map'),
    url(r'^ajax/template/cabinet/publications/unpublished/photos/$', 'templates.publications.unpublished_photos'),


    # settings
    url(r'^ajax/template/cabinet/settings/$', 'templates.settings.settings'),


    # support
    url(r'^ajax/template/cabinet/support/$', 'templates.support.support'),
    url(r'^ajax/template/cabinet/support/ticket/$', 'templates.support.ticket'),


	# published publications forms
    url(r'^ajax/template/cabinet/publications/published/$', 'templates.publications.published_form'),


    # # hints
    # url(r'^ajax/template/cabinet/publications/hints/no-publications/$', 'publications.no_pubs_hint'),
    # url(r'^ajax/template/cabinet/support/hints/no-tickets/$', 'support.no_tickets_hint'),
)