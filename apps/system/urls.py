# coding=utf-8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('apps.system',

   #API
   url(r'', include('apps.system.api.escaped_fragments.urls')),

)
