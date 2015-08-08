#coding=utf-8
from django.core.management import BaseCommand

from core.markers_index.models import SegmentsIndex
from core.publications.constants import HEAD_MODELS


class Command(BaseCommand):
    def handle(self, *args, **options):
        SegmentsIndex.clear()

        for tid, model in HEAD_MODELS.iteritems():
            for publication in model.all_published():
                publication.unpublish()
                print('publication {0}:{1} unpublished'.format(tid, publication.id))

                publication.publish(pub_date_should_be_updated=False)
                print('publication {0}:{1} published back. OK'.format(tid, publication.id))
