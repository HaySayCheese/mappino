# coding=utf-8
import itertools
from collections import Counter

from datetime import timedelta
from django.core.management import BaseCommand
from django.utils.timezone import now

from core.publications.constants import LIVING_HEAD_MODELS, \
    LIVING_RENT_PUBLICATION_MAY_BE_ACTIVE, LIVING_SALE_PUBLICATION_MAY_BE_ACTIVE, \
    COMMERCIAL_RENT_PUBLICATION_MAY_ACTIVE, COMMERCIAL_SALE_PUBLICATION_MAY_ACTIVE
from core.users.models import Users
from core.users.notifications.sms_dispatcher.senders.base import TimeGentleSMSSender


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Searching for possible outdated publications is started..')

        today = now().date()

        #
        # check living rent publications
        living_rent_min_published_date = \
            today - timedelta(days=LIVING_RENT_PUBLICATION_MAY_BE_ACTIVE)

        living_rent_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            living_rent_owners_ids += model.objects\
                .filter(for_rent=True, published__lt=living_rent_min_published_date)\
                .values_list('owner_id', flat=True)

        #
        # check living sale publications
        living_sale_min_published_date = \
            today - timedelta(days=LIVING_SALE_PUBLICATION_MAY_BE_ACTIVE)

        living_sale_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            living_sale_owners_ids += model.objects\
                .filter(for_sale=True, published__lt=living_sale_min_published_date)\
                .values_list('owner_id', flat=True)

        #
        # check commercial rent publications
        commercial_rent_min_published_date = \
            today - timedelta(days=COMMERCIAL_RENT_PUBLICATION_MAY_ACTIVE)

        commercial_rent_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            commercial_rent_owners_ids += model.objects\
                .filter(for_rent=True, published__lt=commercial_rent_min_published_date)\
                .values_list('owner_id', flat=True)

        #
        # check living commercial publications
        commercial_sale_min_published_date = \
            today - timedelta(days=COMMERCIAL_SALE_PUBLICATION_MAY_ACTIVE)

        commercial_sale_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            commercial_sale_owners_ids += model.objects\
                .filter(for_sale=True, published__lt=commercial_sale_min_published_date)\
                .values_list('owner_id', flat=True)

        # calculating how much possible inactive publications have every owner
        counter = Counter(
            itertools.chain(
                living_rent_owners_ids, living_sale_owners_ids,
                commercial_rent_owners_ids, commercial_sale_owners_ids))

        for owner_id, possible_inactive_publications_count in counter.iteritems():
            user_mobile_phone = Users.objects\
                .filter(id=owner_id)\
                .values_list('mobile_phone', flat=True)\
                [:1][0]

            if possible_inactive_publications_count > 1:
                TimeGentleSMSSender.process_transaction(
                    user_mobile_phone,
                    'Похоже, что Вы давно не продлевали несколько своих объявлений. '
                    'Пожалуйста, зайдите в личный кабинет mappino, чтобы автоматически продлить их.')

            elif possible_inactive_publications_count == 1:
                TimeGentleSMSSender.process_transaction(
                    user_mobile_phone,
                    'Похоже, что Вы давно не продлевали одно из своих объявлений. '
                    'Пожалуйста, зайдите в личный кабинет mappino, чтобы автоматически продлить его.')

            print('User {phone} is alerted about {count} publication(s).'.format(
                phone=user_mobile_phone, count=possible_inactive_publications_count))

        print('Searching is finished.')
