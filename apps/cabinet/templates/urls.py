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


urlpatterns += patterns('apps.cabinet.templates.managers',

    # users
    url(r'^ajax/template/cabinet/managers/users/$', 'users'),

    # settings
    url(r'^ajax/template/cabinet/managers/settings/$', 'settings'),

    #briefs
    url(r'^ajax/template/cabinet/managers/briefs/$', 'briefs'),

    #publication
    url(r'^ajax/template/cabinet/managers/publication/$', 'publication'),

    # unpublished publications forms
    url(r'^ajax/template/cabinet/managers/publications/unpublished/(\d+)/$', 'publications_unpublished_form'),
    url(r'^ajax/template/cabinet/managers/publications/unpublished/footer/$', 'publications_unpublished_footer'),

)