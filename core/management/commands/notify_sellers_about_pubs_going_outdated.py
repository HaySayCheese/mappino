# coding=utf-8
from collections import Counter

import itertools
from datetime import timedelta
from django.core.management import BaseCommand
from django.utils.timezone import now

from core.publications.constants import LIVING_HEAD_MODELS
from core.users.models import Users
from core.users.notifications.sms_dispatcher.models import SendQueue


class Command(BaseCommand):
    living_rent_publication_may_be_active = 14     # days
    living_sale_publication_may_be_active = 30     # days

    commercial_rent_publication_may_active = 30    # days
    commercial_sale_publication_may_active = 45    # days

    def handle(self, *args, **options):
        print('Searching for possible outdated publications is started.')

        today = now().date()

        #
        # check living rent publications
        living_rent_min_published_date = \
            today - timedelta(days=self.living_rent_publication_may_be_active)

        living_rent_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            living_rent_owners_ids += model.objects\
                .filter(for_rent=True, published__lt=living_rent_min_published_date)\
                .values_list('owner_id', flat=True)

        #
        # check living sale publications
        living_sale_min_published_date = \
            today - timedelta(days=self.living_sale_publication_may_be_active)

        living_sale_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            living_sale_owners_ids += model.objects\
                .filter(for_sale=True, published__lt=living_sale_min_published_date)\
                .values_list('owner_id', flat=True)

        #
        # check commercial rent publications
        commercial_rent_min_published_date = \
            today - timedelta(days=self.commercial_rent_publication_may_active)

        commercial_rent_owners_ids = []
        for _, model in LIVING_HEAD_MODELS.iteritems():
            commercial_rent_owners_ids += model.objects\
                .filter(for_rent=True, published__lt=commercial_rent_min_published_date)\
                .values_list('owner_id', flat=True)

        #
        # check living sale publications
        commercial_sale_min_published_date = \
            today - timedelta(days=self.commercial_sale_publication_may_active)

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
                SendQueue.enqueue(
                    'Похоже, что Вы давно не продлевали несколько своих объявлений. '
                    'Пожалуйста, зайдите в личный кабинет mappino, чтобы автоматически продлить их.',
                    user_mobile_phone, today)

            elif possible_inactive_publications_count == 1:
                SendQueue.enqueue(
                    'Похоже, что Вы давно не продлевали одно из своих объявлений. '
                    'Пожалуйста, зайдите в личный кабинет mappino, чтобы автоматически продлить его.',
                    user_mobile_phone, today)

            print('User {phone} is alerted about {count} publication(s).'.format(
                phone=user_mobile_phone, count=possible_inactive_publications_count))

        print('Searching is finished.')
