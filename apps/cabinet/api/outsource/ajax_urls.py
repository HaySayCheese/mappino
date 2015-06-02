from apps.cabinet.api.outsource.photographers.ajax import PhotographersOrdersView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/outsource/photographers/$', PhotographersOrdersView.as_view()),
    )