#coding=utf-8
from django.db import models, IntegrityError
from djorm_expressions.models import ExpressionManager
from collective.exceptions import AlreadyExist, RecordAlreadyExists, RecordDoesNotExists
from core.constants import HEAD_MODELS, OBJECTS_TYPES
from core.dirtags.constants import DIR_TAGS_COLORS
from core.users.models import Users



class PublicationAlreadyExists(AlreadyExist): pass

class DirTags(models.Model):
	user = models.ForeignKey(Users)
	title = models.TextField(db_index=True)
	color_id = models.SmallIntegerField()
	pubs = models.TextField(db_index=True)

	objects = ExpressionManager()

	class Meta:
		db_table = 'dir_tags'
		unique_together = (('user', 'title'), )


	@classmethod
	def new(cls, user_id, title, color_id):
		if not title:
			raise ValueError('Title can not be empty.')

		title = title.lstrip().rstrip()
		if not title:
			raise ValueError('Title contains only spaces.')

		if color_id not in DIR_TAGS_COLORS.values():
			raise ValueError('Invalid @color_id')

		try:
			return cls.objects.create(
				user_id = user_id,
				title = title,
			    color_id = color_id,
			)
		except IntegrityError:
			raise RecordAlreadyExists()


	@classmethod
	def by_id(cls, tag_id):
		return DirTags.objects.get(id = tag_id)


	@classmethod
	def by_user_id(cls, user_id):
		return DirTags.objects.filter(user_id = user_id)


	@staticmethod
	def rm_all_publication_occurrences(tid, hid):
		"""
		Видалить всі входження оголошення з id=hid та типом=tid з тегів всіх користувачів.
		Даний метод викликаєтсья при фізичному видаленні оголошення з БД
		для забезпечення цілісності системи.
		"""
		for tag in DirTags.objects.filter(pubs__contains = DirTags.__to_record_format(tid, hid)):
			tag.rm_publication(tid, hid)


	def publications(self):
		"""
		Якщо раніше було додано хочаб одне оголошення -
		поверне словник формату "id типу: QuerySet head-записів даного типу".
		Якщо пов’язаних оголошень немає - поверне пустий словник.
		"""
		if not self.pubs:
			return dict()

		results = {}
		for pub in self.pubs.split(','):
			tid, hid = self.__to_tid_and_hid(pub)
			if tid in results:
				results[tid].append(hid)
			else:
				results[tid] = [hid]

		for tid, head_ids in results.items():
			results[tid] = HEAD_MODELS[tid].objects.filter(id__in = head_ids)
		return results


	def add_publication(self, tid, hid):
		"""
		Додає посилання на head-запис оголошення в поточний тег.
		Перед додаванням буде здійснено перевірку чи оголошення існує в БД.
		"""
		if tid not in OBJECTS_TYPES.values():
			raise ValueError('@tid is not correct object type.')

		model = HEAD_MODELS[tid]
		if model.objects.filter(id=hid).count() == 0:
			raise ValueError('Record with @hid is absent in table.')

		if not self.pubs:
			self.pubs = self.__to_record_format(tid, hid)
			self.save(force_update=True)
		else:
			record = self.__to_record_format(tid, hid)
			if record not in self.pubs:
				self.pubs += (',' + record)
				self.save(force_update=True)
			else:
				raise PublicationAlreadyExists('@hid already exists in tag.')


	def rm_publication(self, tid, hid):
		"""
		Видалить посилання на head-запис оголошення з тегу.
		Перевірка чи оголошення існує в БД проведено не буде.
		"""
		record = self.__to_record_format(tid, hid)
		if not record in self.pubs:
			raise RecordDoesNotExists()

		self.pubs = self.pubs.replace(record, '')
		if self.pubs:
			if self.pubs[-1] == ',':
				self.pubs = self.pubs[:-1]
			else:
				self.pubs = self.pubs.replace(',,', ',')
		self.save(force_update=True)


	def clear_publications(self):
		"""
		Видалить всі посилання на всі head-записи оголошень.
		"""
		self.pubs = ''
		self.save()


	@staticmethod
	def __to_record_format(tid, hid):
		"""
		Поверне запис, під яким слід зберегти посилання на оголошення.
		"""
		return str(tid) + ':' + str(hid)


	@staticmethod
	def __to_tid_and_hid(record):
		"""
		Поверне tid та hid оголошення, конвертнувши їх із запису record.
		"""
		tid, hid = record.split(':')
		return int(tid), int(hid)

