#coding=utf-8
#
# Даний модуль забезпечує сканування ajax-сторінок сайту за механізмом escaped_fragment.
# Кожного разу при публікації оголошення воно заноситься в чергу на індексацію.
# Далі запускається граббер на клієнті, який запитує пачками по пару штук tid та hash_id оголошень,
# грабить їх html та відсилає назад на сервер, де вони gzip'ляться і скаладаються на віддачу пошуковим машинам.
#
from django.conf import settings
from django.dispatch import receiver
import os

from core.publications import models_signals
from core.escaped_fragments_manager.models import SEIndexerQueue


@receiver(models_signals.published)
def add_publication_to_index_queue(sender, **kwargs):
	SEIndexerQueue.add(kwargs['tid'], kwargs['hash_id'])


@receiver(models_signals.unpublished)
@receiver(models_signals.deleted_permanent)
def remove_publication_to_index_queue(sender, **kwargs):
	tid, hash_id = kwargs['tid'], kwargs['hash_id']

	# removing the publication from grabber's queue
	SEIndexerQueue.remove(tid, hash_id)

	# removing the snapshot from the FS
	escaped_fragment = os.path.join(
		settings.BASE_DIR, 'static', 'escaped_fragments', 'publication', '{0}:{1}'.format(tid, hash_id))

	try:
		os.remove(escaped_fragment)
	except Exception:
		# the fragment may be absent if grabber does not indexed this publication yet.
		pass



