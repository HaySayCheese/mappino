from django.dispatch import receiver
from core.publications import models_signals
from core.escaped_fragments_manager.models import SEIndexerQueue



# init signals
@receiver(models_signals.published)
def add_publication_to_index_queue(sender, **kwargs):
	SEIndexerQueue.add(kwargs['tid'], kwargs['hash_id'])


@receiver(models_signals.unpublished)
@receiver(models_signals.deleted_permanent)
def remove_publication_to_index_queue(sender, **kwargs):
	SEIndexerQueue.remove(kwargs['tid'], kwargs['hid'])


