# coding=utf-8

from datetime import timedelta
from django.core.management import BaseCommand
from django.utils.timezone import now

from core.publications.constants import LIVING_HEAD_MODELS, \
    LIVING_RENT_PUBLICATION_MAY_BE_ACTIVE, LIVING_SALE_PUBLICATION_MAY_BE_ACTIVE, \
    COMMERCIAL_RENT_PUBLICATION_MAY_ACTIVE, COMMERCIAL_SALE_PUBLICATION_MAY_ACTIVE


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Searching for possible outdated publications is started..')

        today = now().date()

        #
        # check living rent publications
        living_rent_min_published_date = \
            today - timedelta(days=LIVING_RENT_PUBLICATION_MAY_BE_ACTIVE)

        for tid, model in LIVING_HEAD_MODELS.iteritems():
            outdated_pubs = model.objects.filter(for_rent=True, published__lt=living_rent_min_published_date)
            for pub in outdated_pubs:
                pub.mark_as_outdated_and_unpublish()
                print('Publication {tid}:{hash_id} was marked as outdated and unpublished.'.format(
                    tid=tid, hash_id=pub.hash_id))

        #
        # check living sale publications
        living_sale_min_published_date = \
            today - timedelta(days=LIVING_SALE_PUBLICATION_MAY_BE_ACTIVE)

        for tid, model in LIVING_HEAD_MODELS.iteritems():
            outdated_pubs = model.objects.filter(for_sale=True, published__lt=living_sale_min_published_date)
            for pub in outdated_pubs:
                pub.mark_as_outdated_and_unpublish()
                print('Publication {tid}:{hash_id} was marked as outdated and unpublished.'.format(
                    tid=tid, hash_id=pub.hash_id))

        #
        # check commercial rent publications
        commercial_rent_min_published_date = \
            today - timedelta(days=COMMERCIAL_RENT_PUBLICATION_MAY_ACTIVE)

        for tid, model in LIVING_HEAD_MODELS.iteritems():
            outdated_pubs = model.objects.filter(for_rent=True, published__lt=commercial_rent_min_published_date)
            for pub in outdated_pubs:
                pub.mark_as_outdated_and_unpublish()
                print('Publication {tid}:{hash_id} was marked as outdated and unpublished.'.format(
                    tid=tid, hash_id=pub.hash_id))

        #
        # check commercial sale publications
        commercial_sale_min_published_date = \
            today - timedelta(days=COMMERCIAL_SALE_PUBLICATION_MAY_ACTIVE)

        for tid, model in LIVING_HEAD_MODELS.iteritems():
            outdated_pubs = model.objects.filter(for_sale=True, published__lt=commercial_sale_min_published_date)
            for pub in outdated_pubs:
                pub.mark_as_outdated_and_unpublish()
                print('Publication {tid}:{hash_id} was marked as outdated and unpublished.'.format(
                    tid=tid, hash_id=pub.hash_id))

        print('Searching is finished.')
