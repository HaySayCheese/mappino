# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import Manager
from django.utils.timezone import now

from collective.utils import generate_sha256_unique_id
from core.moderators.classes import RedisHandler
from core.moderators.models_abstract import AbstractPublicationModel, AbstractProcessedPublicationModel
from core.publications.constants import HEAD_MODELS
from core.users.models import Users



class PublicationsCheckQueue(AbstractPublicationModel):
    class Meta:
        db_table = 'moderators_publications_check_queue'
        unique_together = (('publication_tid', 'publication_hash_id'), )


    @classmethod
    def next_record(cls, moderator):
        # if moderator already have one publication bound for himself -
        # then he must proceed with it.
        bound_record = cls.__record_bound_by_moderator(moderator)
        if bound_record:
            return bound_record


        # claimed records should be processed firstly
        claimed_record = cls.__record_with_claims(moderator)
        if claimed_record:
            return claimed_record


        regular_record = cls.__regular_record(moderator)
        if regular_record:
            return regular_record


        # no records for check
        return None


    def accept(self, moderator):
        self.publication.reject_by_moderator()

        AcceptedPublications.objects.add(self.publication_tid, self.publication_hash_id, moderator.id)
        RedisHandler.unbind_from_the_moderator(moderator, self.publication_tid, self.publication_hash_id)

        self.__close_all_claims(moderator)
        self.delete()


    def reject(self, moderator, message):
        RejectedPublications.objects.add(
            self.publication_tid, self.publication_hash_id, moderator.id, message) # note message here
        RedisHandler.unbind_from_the_moderator(moderator, self.publication_tid, self.publication_hash_id)

        # note: no claims closing is needed
        self.delete()


    def hold(self, moderator):
        PublicationsHeld.objects.add(self.publication_tid, self.publication_hash_id, moderator.id)
        RedisHandler.unbind_from_the_moderator(moderator, self.publication_tid, self.publication_hash_id)

        # note: no claims closing is needed
        self.delete()


    def claims(self):
        return PublicationsClaims.objects.by_publication(self.publication_tid, self.publication_hash_id)


    @classmethod
    def __record_bound_by_moderator(cls, moderator):
        publications_ids = RedisHandler.publications_bound_by_moderator(moderator)
        if not publications_ids:
            # if no ids has been received - than Q-object will be build empty,
            # and, as a result, - filter() will be called with empty condition.
            return None


        for tid, hash_id, _ in publications_ids:
            try:
                return cls.objects.get(publication_tid=tid, publication_hash_id=hash_id)

            except ObjectDoesNotExist:
                # redis contains invalid binding
                RedisHandler.unbind_from_the_moderator(moderator, tid, hash_id)

        return None


    @classmethod
    def __record_with_claims(cls, moderator):
        # filter only publications with claims
        claimed_publications_ids = PublicationsClaims.objects\
            .filter(date_closed__isnull=True)\
            .values_list('publication_tid', 'publication_hash_id')\
            .distinct()

        if not claimed_publications_ids:
            # if no ids has been received - than Q-object will be build empty,
            # and, as a result, - filter() will be called with empty condition.
            return None

        else:
            query = cls.objects.filter_by_publications_ids(claimed_publications_ids)


        # exclude all publications that are already bound to moderators
        already_bound_publications_ids = RedisHandler.all_bound_publications()
        if already_bound_publications_ids:
            # if no ids has been received - than Q-object will be build empty,
            # and, as a result, - exclude() will be called with empty filter.

            query &= cls.objects.exclude_publications_ids(already_bound_publications_ids)


        try:
            claimed_record = query[:1][0]
            RedisHandler.bind_to_the_moderator(
                moderator, claimed_record.publication_tid, claimed_record.publication_hash_id) # prolong binding
            return claimed_record

        except IndexError:
            return None


    @classmethod
    def __regular_record(cls, moderator):
        # exclude all publications that are already bound to moderators
        already_bound_publications_ids = RedisHandler.all_bound_publications()

        try:
            record = cls.objects.exclude_publications_ids(already_bound_publications_ids)[:1][0]
            RedisHandler.bind_to_the_moderator(moderator, record.publication_tid, record.publication_hash_id) # prolong binding
            return record

        except IndexError:
            return None


    def __close_all_claims(self, moderator):
        for claim in PublicationsClaims.objects.by_publication(self.publication_tid, self.publication_hash_id):
            claim.close(moderator)



class RejectedPublications(AbstractProcessedPublicationModel):
    message = models.TextField()


    class Meta:
        db_table = 'moderators_publications_rejected'


    class ObjectsManager(Manager):
        def add(self, *args):
            return self.create(
                publication_tid = args[0],
                publication_hash_id = args[1],
                moderator_id = args[2],
                message = args[3],
            )


        def by_moderator(self, moderator):
            return self.filter(moderator_id=moderator)


    objects = ObjectsManager()


    @classmethod
    def moderator_message_for_publication(cls, tid, hash_id):
        try:
            return cls.objects.filter(publication_tid=tid, publication_hash_id=hash_id)[:1][0].message
        except IndexError:
            return None


class AcceptedPublications(AbstractProcessedPublicationModel):
    class Meta:
        db_table = 'moderators_publications_accepted'



class PublicationsHeld(AbstractProcessedPublicationModel):
    class Meta:
        db_table = 'moderators_publications_held'



class PublicationsClaims(models.Model):
    hash_id = models.TextField(default=generate_sha256_unique_id, unique=True)
    reason_tid = models.PositiveSmallIntegerField()
    date_reported = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True)

    email = models.EmailField()
    message = models.TextField(null=True)

    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)

    moderator = models.ForeignKey(Users, null=True, related_name='moderator')
    moderator_notice = models.TextField(null=True)


    class Meta:
        db_table = 'moderators_publications_claims'
        ordering = ['-date_reported', ]


    class ObjectsManager(Manager):
        class Reasons(object):
            other = 0
            owner_is_an_intermediary = 1 # власник оголошення - посередник
            untruthful_content = 2
            photos_do_not_correspond_to_reality = 3


        class Messages(object):
            @staticmethod
            def owner_is_intermediary():
                # todo: translates must goes here
                return u"владелец объявления - посредник"


            @staticmethod
            def untruthful_content():
                # todo: translates must goes here
                return u"объявление содержит подозрительный контент"


            @staticmethod
            def photos_do_not_correspond_to_reality():
                # todo: translates must goes here
                return u"фото не соответствуют реальности"


        def add(self, publication_tid, publication_hash_id, reason_tid, email, custom_message=None):
            if reason_tid == self.Reasons.owner_is_an_intermediary:
                message = self.Messages.owner_is_intermediary()

            elif reason_tid == self.Reasons.untruthful_content:
                message = self.Messages.untruthful_content()

            elif reason_tid == self.Reasons.photos_do_not_correspond_to_reality:
                message = self.Messages.photos_do_not_correspond_to_reality()

            elif reason_tid == self.Reasons.other:
                message = custom_message

            else:
                raise ValueError('Invalid claim type.')


            with transaction.atomic():
                # add publication to the check queue or update uts date added if it is already exits
                PublicationsCheckQueue.objects.add_or_update(publication_tid, publication_hash_id)

                return self.create(
                    reason_tid = reason_tid,
                    message = message,
                    email = email,

                    publication_tid = publication_tid,
                    publication_hash_id = publication_hash_id,
                )


        def by_publication(self, tid, hash_id):
            return self.filter(publication_tid=tid, publication_hash_id=hash_id)


    objects = ObjectsManager()


    @property
    def publication(self):
        try:
            return HEAD_MODELS[self.publication_tid].objects.get(hash_id=self.publication_hash_id)

        except ObjectDoesNotExist:
            return None


    def close(self, moderator):
        self.moderator = moderator
        self.date_closed = now()
        self.save()