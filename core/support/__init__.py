# coding=utf-8
from django.apps import AppConfig

from core.support.classes import SupportAgentsNotifier


class SupportApp(AppConfig):
    name = 'core.support'
    agents_notifier = SupportAgentsNotifier()