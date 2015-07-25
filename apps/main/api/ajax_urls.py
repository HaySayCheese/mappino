#coding=utf-8
from django.conf.urls import patterns, url

from apps.main.api.correspondence.ajax import SendMessageFromClient, SendCallRequestFromClient
from apps.main.api.favorites.ajax import FavoritesListView
from apps.main.api.publications_and_markers.ajax import Markers, DetailedView, Claims
from apps.main.api.contacts.ajax import Contacts


urlpatterns = patterns('apps.main.api',
    # markers output
    url(r'^ajax/api/markers/$', Markers.as_view()),

    # detailed publication view
    url(r'^ajax/api/detailed/publication/(\d+):(\w+)/$', DetailedView.as_view()),

    # contacts
    url(r'^ajax/api/detailed/publication/(\d+):(\w+)/contacts/$', Contacts.as_view()),

    # correspondence
    url(r'^ajax/api/notifications/send-message/(\d+:\w+)/$', SendMessageFromClient.as_view()),
    url(r'^ajax/api/notifications/send-call-request/(\d+:\w+)/$', SendCallRequestFromClient.as_view()),

    # favorites
    url(r'^ajax/api/favorites/$', FavoritesListView.as_view()),
    url(r'^ajax/api/favorites/(\d+):(\w+)/$', FavoritesListView.as_view()),

    # #viewed
    # url(r'^ajax/api/viewed/$', ViewedPublicationsView.as_view()),
    # url(r'^ajax/api/viewed/(\d+):(\w+)/$', ViewedPublicationsView.as_view()),

    # claims
    url(r'^ajax/api/publications/(\d+):(\w+)/claims/$', Claims.List.as_view()),
)