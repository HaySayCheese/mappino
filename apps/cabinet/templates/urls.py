# coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet.templates.templates',
    # briefs
    url(r'^ajax/template/cabinet/publications/briefs/$', 'publications_briefs'),

    # publication
    url(r'^ajax/template/cabinet/publications/publication/$', 'publications_publication'),


    # unpublished publications forms
    url(r'^ajax/template/cabinet/publications/unpublished/(\d+)/$', 'publications_unpublished_form'),
    url(r'^ajax/template/cabinet/publications/unpublished/footer/$', 'publications_unpublished_footer'),


    # published publications forms
    # url(r'^ajax/template/cabinet/publications/published/$', ''), # todo: fix me


    # settings
    url(r'^ajax/template/cabinet/settings/$', 'settings'),


    # support
    url(r'^ajax/template/cabinet/support/$', 'support'),
    url(r'^ajax/template/cabinet/support/ticket/$', 'support_ticket'),


    # # hints
    # url(r'^ajax/template/cabinet/publications/hints/no-publications/$', 'publications.no_pubs_hint'),
    # url(r'^ajax/template/cabinet/support/hints/no-tickets/$', 'support.no_tickets_hint'),
)