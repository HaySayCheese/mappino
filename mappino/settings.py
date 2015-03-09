#coding=utf-8

#
# https://docs.djangoproject.com/en/1.6/ref/settings/
#

DEBUG = False
if not DEBUG:
	from production_settings import *
else:
	from dev_settings import *