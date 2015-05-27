from django.db import models
import datetime
class PublicationsToCheck(models.Model):

    publication_hash_id = models.TextField(db_index=True)
    publication_type_id = models.IntegerField(db_index=True)
    is_suspicious = models.BooleanField(default=False)
    date_added = models.DateTimeField()



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
