import datetime
from django.conf import settings
from django.http.response import HttpResponse
from os import walk
from django.views.generic import View
from xml.etree.ElementTree import Element, SubElement, tostring
import os
import time


class SitemapView(View):
	@staticmethod
	def get(request):
		path = os.path.join(settings.BASE_DIR, 'static', 'escaped_fragments')
		files = []
		for (dirpath, dirnames, filenames) in walk(path):
			files.extend(filenames)
			break


		urlset = Element('urlset')
		for filename in files:
			url = SubElement(urlset, "url")

			loc = SubElement(url, 'loc')
			loc.text = "/#!/publication/{0}".format(filename[:-3])

			lastmod = SubElement(url, 'lastmod')
			lastmod.text = ':%Y-%m-%d'.format(time.ctime(os.path.getmtime(os.path.join(path, filename))))

			changefreq = SubElement(url, 'changefreq')
			changefreq.text = 'monthly'

			priority = SubElement(url, 'priority')
			priority.text = '0.5'


		xml = '<?xml version="1.0" encoding="UTF-8"?>' + tostring(urlset)
		return HttpResponse(xml, 'application/xml')