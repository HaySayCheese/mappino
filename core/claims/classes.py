#coding=utf-8
from core.claims.models import PublicationsClaims
from core.email_backend.utils import ModeratorsNotifier
from core.publications.constants import HEAD_MODELS


class ClaimsManager(object):
    class PublicationDoesNotExists(Exception): pass
    class InvalidPublicationTypeId(ValueError): pass
    class InvalidUserEmail(ValueError): pass
    class InvalidClaimTypeId(ValueError): pass


    @classmethod
    def claim(cls, publication_tid, publication_hash_id, user_email, claim_tid, custom_message=None):
        if not user_email:
            raise cls.InvalidUserEmail()

        model = HEAD_MODELS.get(publication_tid)
        if not model:
            raise cls.InvalidPublicationTypeId()

        publication = model.objects.filter(hash_id=publication_hash_id).only('id', 'owner', 'owner__id')[:1]
        if not publication:
            raise ClaimsManager.PublicationDoesNotExists()
        else:
            publication = publication[0]


        try:
            claim = PublicationsClaims.new(
                publication_tid, publication.id, publication.owner.id, claim_tid, custom_message
            )
            ModeratorsNotifier.publication_claimed(publication_tid, publication_hash_id, claim.owner, claim.message)
        except PublicationsClaims.InvalidClaimTypeId:
            return cls.InvalidClaimTypeId