import datetime

from django.db import models
from core.users.models import Users


class PublicationsToCheck(models.Model):

    publication_hash_id = models.TextField()
    publication_type_id = models.IntegerField()
    is_suspicious = models.BooleanField(db_index=True, default=False)
    date_added = models.DateTimeField(db_index=True)
    moderated_by = models.ForeignKey(Users)
    date_moderated = models.DateTimeField(db_index=True, null=True)

    class Meta:
        db_table = 'moderators_publications_to_check'
        unique_together=(('publication_hash_id', 'publication_type_id'),)


    @classmethod
    def add(cls, publication_type_id, publication_hash_id, is_suspicious):
        try:
            record = cls.objects.filter(
                publication_type_id = publication_type_id,
                publication_hash_id = publication_hash_id
                    ).only('publication_ids')[:1][0]

            record.is_suspicious = is_suspicious
            record.save()
        except IndexError:
            record = cls.objects.create(
                publication_type_id = publication_type_id,
                publication_hash_id = publication_hash_id,
                is_suspicious = is_suspicious,
                date_added = datetime.datetime.now()
            )

        return record

    @classmethod
    def remove(cls, publication_type_id, publication_hash_id):
        cls.objects.filter(
            publication_type_id = publication_type_id,
            publication_hash_id = publication_hash_id)\
            .delete()


    @classmethod
    def get_publication_for_moderate(cls, moderator_id):

        try:
            #We will check if moderator finished last publication that he took
            return cls.objects.filter(
                moderated_by = moderator_id,
                date_moderated = None)[:1][0]

        except IndexError:
            pass


        try:
            #todo Check waht will be first. update or limit.
            return PublicationsToCheck.objects\
                .filter(date_moderated = None)\
                .order_by('is_suspicious', 'date_added')\
                .update(moderated_by = moderator_id)[:1]

        except IndexError:
            return cls.objects.none()














































