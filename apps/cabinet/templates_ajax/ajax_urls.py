# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.cabinet.templates_ajax',
    url(r'^ajax/template/cabinet/briefs/$', 'publications.briefs_template'),


    # url(r'^ajax/template/cabinet/publications/$', 'publications.publications_panel_template'),


    # unpublished forms
    url(r'^ajax/template/cabinet/publications/unpublished/(\d+)/$', 'publications.unpublished_form_template'),
    url(r'^ajax/template/cabinet/publications/unpublished/map/$', 'publications.unpublished_map_template'),
    url(r'^ajax/template/cabinet/publications/unpublished/photos/$', 'publications.unpublished_photos_template'),


	# published publications forms
    url(r'^ajax/template/cabinet/publications/published/$', 'publications.published_form_template'),


    # settings
    url(r'^ajax/template/cabinet/settings/$', 'settings.settings_template'),


    # support
    url(r'^ajax/template/cabinet/support/$', 'support.support_template'),
    url(r'^ajax/template/cabinet/support/ticket/$', 'support.ticket_template'),


    # hints
    url(r'^ajax/template/cabinet/publications/hints/no-publications/$', 'publications.no_pubs_hint'),
    url(r'^ajax/template/cabinet/support/hints/no-tickets/$', 'support.no_tickets_hint'),
)