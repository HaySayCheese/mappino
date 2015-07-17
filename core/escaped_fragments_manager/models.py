from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.utils import DatabaseError


class SEIndexerQueue(models.Model):
	tid = models.SmallIntegerField()
	hash_id = models.TextField()

	class Meta:
		db_table = 'se_indexer_queue'
		unique_together = (
			('tid', 'hash_id'),
		)
		index_together = (
			('tid', 'hash_id'),
		)


	@classmethod
	def add(cls, tid, hash_id):
		try:
			cls.objects.create(
				tid=tid,
			    hash_id=hash_id,
			)
		except DatabaseError:
			pass


	@classmethod
	def remove(cls, tid, hash_id):
		try:
			cls.objects.get(tid=tid, hash_id=hash_id).delete()
		except ObjectDoesNotExist:
			pass


	@classmethod
	def next_queued_publications_pack(cls):
		return [(p.tid, p.hash_id) for p in cls.objects.all()]