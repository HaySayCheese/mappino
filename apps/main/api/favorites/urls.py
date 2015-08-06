#coding=utf-8
from django.conf.urls import patterns, url

from apps.main.api.favorites.ajax import FavoritesListView


urlpatterns = patterns('',
    url(r'^ajax/api/user/favorites/$', FavoritesListView.as_view()),
    url(r'^ajax/api/user/favorites/(\d+):(\w+)/$', FavoritesListView.as_view()),
)