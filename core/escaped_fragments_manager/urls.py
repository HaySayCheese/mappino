from django.conf.urls import patterns, url, include
from core.escaped_fragments_manager.ajax import GrabberView
from core.escaped_fragments_manager.views import SitemapView


urlpatterns = patterns('core',
	# sitemap
    url(r'^sitemap.xml$', SitemapView.as_view()),


    # grabber
    url(r'^ajax/api/grabber/iMvorMXScUgbbDGuJGCbnTnQwPRFKk/$', GrabberView.as_view()),
)
