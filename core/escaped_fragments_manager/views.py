#coding=utf-8
from xml.etree.ElementTree import Element, SubElement, tostring
import time

from django.conf import settings
from django.http.response import HttpResponse
from os import walk
from django.views.generic import View
import os


class SitemapView(View):
	def get(self, request):
		# sitemap.xml generation
		urlset = Element('urlset')
		urlset.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"


		# todo: додати посилання на домашню сторінку
		self.__add_url(urlset, "{domain}/promo/".format(domain=settings.MAIN_DOMAIN), priority='0.7')
		self.__add_url(urlset, "{domain}/promo/realtors/".format(domain=settings.MAIN_DOMAIN), priority='0.8')


		# inserting publication's urls into sitemap.xml
		files = []
		fragments_root = os.path.join(settings.BASE_DIR, 'static', 'escaped_fragments', 'publication')
		for (_, __, filenames) in walk(fragments_root):
			files.extend(filenames)
			break

		for filename in files:
			loc = "{domain}/#!/publication/{0}/".format(filename[:-3], domain=settings.MAIN_DOMAIN)
			lastmod = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(os.path.join(fragments_root, filename))))
			changefreq = 'monthly'
			priority = '0.5'

			self.__add_url(urlset, loc, lastmod, changefreq, priority)


		xml = '<?xml version="1.0" encoding="UTF-8"?>' + tostring(urlset)
		return HttpResponse(xml, 'application/xml')


	@staticmethod
	def __add_url(urlset, loc, lastmod=None, changefreq=None, priority=None):
		url = SubElement(urlset, "url")

		_loc = SubElement(url, 'loc')
		_loc.text = loc

		if lastmod:
			_lastmod = SubElement(url, 'lastmod')
			_lastmod.text = lastmod

		if changefreq:
			_changefreq = SubElement(url, 'changefreq')
			_changefreq.text = changefreq

		if priority:
			_priority = SubElement(url, 'priority')
			_priority.text = priority