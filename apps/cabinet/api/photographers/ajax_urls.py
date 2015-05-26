from apps.cabinet.api.photographers.ajax import PhotographersOrdersView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^ajax/api/cabinet/photographers/$', PhotographersOrdersView.as_view()),
    )