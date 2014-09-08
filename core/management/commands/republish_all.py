from django.core.management import BaseCommand
from django.db import transaction

from core.publications.constants import HEAD_MODELS


class Command(BaseCommand):
	def handle(self, *args, **options):
		with transaction.atomic():
			for tid, model in HEAD_MODELS.iteritems():
				for publication in model.all_published():
					publication.unpublish()
					print('publication {0}:{1} unpublished'.format(tid, publication.id))

					publication.publish(update_pub_date=False)
					print('publication {0}:{1} published back. OK'.format(tid, publication.id))
