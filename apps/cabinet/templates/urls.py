# coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet.templates.users',
    # briefs
    url(r'^ajax/template/cabinet/publications/briefs/$', 'publications_briefs'),

    # publication
    url(r'^ajax/template/cabinet/publications/publication/$', 'publications_publication'),


    # unpublished publications forms
    url(r'^ajax/template/cabinet/publications/unpublished/(\d+)/$', 'publications_unpublished_form'),
    url(r'^ajax/template/cabinet/publications/unpublished/footer/$', 'publications_unpublished_footer'),


    # published forms
    url(r'^ajax/template/cabinet/publications/published/$', 'publications_published_form'),


    # rent calendar templates
    url(r'^ajax/template/cabinet/publications/rent-calendar/calendar/$', 'calendar'),
    url(r'^ajax/template/cabinet/publications/rent-calendar/calendar-view/$', 'calendar_view'),


    # settings
    url(r'^ajax/template/cabinet/settings/$', 'settings'),


    # support
    url(r'^ajax/template/cabinet/support/$', 'support'),
    url(r'^ajax/template/cabinet/support/ticket/$', 'support_ticket'),
)


urlpatterns += patterns('apps.cabinet.templates.moderators',
    # moderating
    url(r'^ajax/template/cabinet/moderators/publication/$', 'publication'),
    url(r'^ajax/template/cabinet/moderators/held-publications/$', 'held_publications'),


    # settings
    url(r'^ajax/template/cabinet/moderators/settings/$', 'settings'),
)