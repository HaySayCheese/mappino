# coding=utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('apps.cabinet',
   # flatpages
   url(r'^cabinet/$', 'views.cabinet'),

   # templates
   url(r'', include('apps.cabinet.templates.urls')),

   # Sellers API
   url(r'', include('apps.cabinet.api.sellers.publications.urls')),
   url(r'', include('apps.cabinet.api.sellers.stats.urls')),
   url(r'', include('apps.cabinet.api.sellers.support.urls')),
   url(r'', include('apps.common.api.settings.urls')),

   # Moderators API
   url(r'', include('apps.cabinet.api.moderators.claims.publications.urls')),
   url(r'', include('apps.cabinet.api.moderators.ban.urls')),
)
