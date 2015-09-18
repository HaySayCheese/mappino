# coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.common.templates',
    url(r'^ajax/template/common/publication-preview/container/$', 'publications_preview.container'),
    url(r'^ajax/template/common/publication-preview/header/$', 'publications_preview.header'),
    url(r'^ajax/template/common/publication-preview/body/$', 'publications_preview.body'),
    url(r'^ajax/template/common/publication-preview/contacts/$', 'publications_preview.contacts'),
    url(r'^ajax/template/common/publication-preview/error/$', 'publications_preview.error'),

    url(r'^ajax/template/common/publication-preview/types/(\d+)/$', 'publications_preview.types'),
)