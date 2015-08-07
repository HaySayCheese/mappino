#coding=utf-8
from collective.utils import generate_sha256_unique_id
from core.users.models import Users
from django.db import models


class PublicationsClaims(models.Model):
    class InvalidClaimTypeId(ValueError): pass


    class States(object):
        new = 0
        processed = 1


    class Types(object):
        other = 0

        owner_is_and_intermediary = 1 # власник оголошення - посередник
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


    #
    # fields
    #
    hash_id = models.TextField(default=generate_sha256_unique_id, unique=True)

    tid = models.PositiveSmallIntegerField()
    date_reported = models.DateTimeField(auto_now_add=True)
    state_sid = models.PositiveSmallIntegerField(db_index=True, default=States.new)

    email = models.EmailField()
    message = models.TextField(null=True)

    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)

    moderator = models.ForeignKey(Users, null=True, related_name='moderator')
    moderator_notice = models.TextField(null=True)
    message_for_owner = models.TextField(null=True)


    class Meta:
        db_table = 'publications_claims'


    @classmethod
    def new(cls, publication_tid, publication_hid, claim_tid, email, custom_message=None):
        if claim_tid == cls.Types.owner_is_and_intermediary:
            message = cls.Messages.owner_is_intermediary()

        elif claim_tid == cls.Types.untruthful_content:
            message = cls.Messages.untruthful_content()

        elif claim_tid == cls.Types.photos_do_not_correspond_to_reality:
            message = cls.Messages.photos_do_not_correspond_to_reality()

        elif claim_tid == cls.Types.other:
            message = custom_message

        else:
            raise cls.InvalidClaimTypeId()


        return cls.objects.create(
            tid = claim_tid,
            message = message,
            email = email,

            publication_tid = publication_tid,
            publication_hash_id = publication_hid,
        )