from django.db import models
from django.utils.timezone import now
from core.users.models import Users


class PublicationsToCheck(models.Model):

    publication_hash_id = models.TextField()
    publication_type_id = models.IntegerField()
    is_suspicious = models.BooleanField(db_index=True, default=False)
    date_added = models.DateTimeField(db_index=True)
    moderated_by = models.ForeignKey(Users, null=True)
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
                date_added = now()
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
            return cls.objects.\
                filter(moderated_by = moderator_id,date_moderated = None).\
                order_by('is_suspicious','date_added')[:1][0]

        except IndexError:
            pass


        try:
             # We have to take last record that was added in table by a set of parameters
             # While this record is taking we locked it for other users, using method update
            if PublicationsToCheck.objects.filter(id__in=cls.objects.filter(date_moderated = None)\
                    .order_by('is_suspicious', 'date_added')[:1]).update(moderated_by = moderator_id):

                # Update return 1. We get our last locked record
                return cls.objects.get(moderated_by = moderator_id,date_moderated = None)

            # If Update return 0 - there are no methods to moderate, so we go out
            return False

        except IndexError:
            return cls.objects.none()



    @classmethod
    def mapped_publication_as_moderated(cls, type_id, hash_id):

            cls.objects.filter(publication_type_id = type_id,publication_hash_id = hash_id)\
            .update(date_moderated = now())



















































