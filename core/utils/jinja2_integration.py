#coding=utf-8
import os
from jinja2 import Environment, FileSystemLoader
from compressor.contrib.jinja2ext import CompressorExtension
from django.conf import settings



environment = Environment(
    loader = FileSystemLoader(os.path.join(settings.BASE_DIR, 'templates')),
    trim_blocks = True,
    lstrip_blocks = True,
    extensions = [CompressorExtension]
)
environment.globals.update({
    'static': settings.STATIC_URL,
})


templates = environment