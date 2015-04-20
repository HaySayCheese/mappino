#coding=utf-8
from core.users.models import Users
from django.db import models


class PublicationsClaims(models.Model):
    class InvalidClaimTypeId(ValueError): pass


    class ClaimTypes(object):
        other = 0
        owner_is_and_intermediary = 1 # власник оголошення - посередник
        untruthful_content = 2
        photos_do_not_correspond_to_reality = 3


    class ClaimMessages(object):
        @staticmethod
        def owner_is_and_intermediary():
            # todo: translates must goes here
            return "оголошення подано від посередника."


        @staticmethod
        def untruthful_content():
            # todo: translates must goes here
            return "оголошення містить неправдивий контент."


        @staticmethod
        def photos_do_not_correspond_to_reality():
            # todo: translates must goes here
            return "фото не відповідають дійсності."


    #
    # fields
    #
    owner = models.ForeignKey(Users)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hid = models.PositiveIntegerField(db_index=True)
    claim_tid = models.PositiveSmallIntegerField()
    message = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'publications_claims'


    @classmethod
    def new(cls, publication_tid, publication_hid, owner_id, claim_tid, custom_message):
        if claim_tid == cls.ClaimTypes.owner_is_and_intermediary:
            message = cls.ClaimMessages.owner_is_and_intermediary()

        elif claim_tid == cls.ClaimTypes.untruthful_content:
            message = cls.ClaimMessages.untruthful_content()

        elif claim_tid == cls.ClaimTypes.photos_do_not_correspond_to_reality:
            message = cls.ClaimMessages.photos_do_not_correspond_to_reality()

        elif claim_tid == cls.ClaimTypes.other:
            message = custom_message

        else:
            raise cls.InvalidClaimTypeId()


        return cls.objects.create(
            publication_tid = publication_tid,
            publication_hid = publication_hid,
            owner_id = owner_id,
            claim_tid = claim_tid,
            message = custom_message
        )