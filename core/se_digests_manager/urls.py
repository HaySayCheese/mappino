from django.conf.urls import patterns, url, include
from core.se_digests_manager.ajax import GrabberView


urlpatterns = patterns('core',
    url(r'^ajax/api/grabber/iMvorMXScUgbbDGuJGCbnTnQwPRFKk/$', GrabberView.as_view()),
)
