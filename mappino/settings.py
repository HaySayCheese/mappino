#coding=utf-8
"""
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

DEBUG = True
if not DEBUG:
	from production_settings import *
else:
	from dev_settings import *