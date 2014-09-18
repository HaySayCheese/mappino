# from django.dispatch import receiver
# from core.cache import counters_cache_manager
# from core.publications import models_signals
#
#
# @receiver(models_signals.)
# @receiver(models_signals.unpublished)
# def publication_unpublished(sender, **kwargs):
# 	counters_cache_manager.increment_etag(kwargs['tid'], kwargs['hash_id'])
#
#
#
#
#
# @receiver(models_signals.before_publish)
# def add_publication_marker(sender, **kwargs):
# 	MARKERS_SERVERS[kwargs['tid']].add_publication(kwargs['hid'])