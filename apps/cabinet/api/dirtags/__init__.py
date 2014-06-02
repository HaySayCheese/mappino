from django.dispatch import receiver
from apps.cabinet.api.dirtags.models import DirTags
from core.publications import models_signals


@receiver(models_signals.deleted_permanent)
def delete_from_dirtags(sender, **kwargs):
	DirTags.rm_all_publication_occurrences(kwargs['tid'], kwargs['hid'])