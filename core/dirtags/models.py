#coding=utf-8
from django.db import models, IntegrityError
from django.db.models import Q
import operator
from collective.exceptions import AlreadyExist, RecordAlreadyExists, RecordDoesNotExists
from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES
from core.dirtags.constants import DIRTAGS_COLORS_IDS
from core.users.models import Users



class PublicationAlreadyExists(AlreadyExist): pass

class DirTags(models.Model):
	separator = ','
	record_separator = ':'

	user = models.ForeignKey(Users)
	title = models.TextField(db_index=True)
	color_id = models.SmallIntegerField()
	pubs = models.TextField(db_index=True)

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

		if color_id not in DIRTAGS_COLORS_IDS.keys():
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
		return cls.objects.get(id = tag_id)


	@classmethod
	def by_user_id(cls, user_id):
		return cls.objects.filter(user_id = user_id)


	@classmethod
	def contains_publications(cls, tid, publications_ids):
		if not publications_ids:
			return cls.objects.none()

		return cls.objects.filter(reduce(operator.or_, (Q(
			pubs__contains=cls.__to_record_format(tid, hid)) for hid in publications_ids)))


	@classmethod
	def rm_all_publication_occurrences(cls, tid, hid):
		"""
		Видалить всі входження оголошення з id=hid та типом=tid з тегів всіх користувачів.
		Даний метод викликаєтсья при фізичному видаленні оголошення з БД
		для забезпечення цілісності системи.
		"""
		tags = DirTags.objects.filter(
			pubs__contains = cls.__to_record_format(tid, hid)).only('id', 'pubs')

		for tag in tags:
			tag.rm_publication(tid, hid)


	def publications_hids(self):
		"""
		Якщо раніше було додано хочаб одне оголошення -
		поверне словник формату "id типу: id head-запису".
		Якщо пов’язаних оголошень немає - поверне пустий словник.
		"""
		if not self.pubs:
			return dict()

		results = {}
		for pub in self.pubs.split(self.separator):
			if not pub:
				continue

			tid, hid = self.__to_tid_and_hid(pub)
			if tid in results:
				results[tid].append(hid)
			else:
				results[tid] = [hid]
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
				self.pubs += (self.separator + record)
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
			if self.pubs[-1] == self.separator:
				self.pubs = self.pubs[:-1]
			elif self.pubs[0] == self.separator:
				self.pubs = self.pubs[1:]
			elif (self.separator + self.separator) in self.pubs:
				self.pubs = self.pubs.replace(self.separator + self.separator, self.separator)
		self.save(force_update=True)


	def clear_publications(self):
		"""
		Видалить всі посилання на всі head-записи оголошень.
		"""
		self.pubs = ''
		self.save()


	def contains(self, tid, hid):
		return self.__to_record_format(tid, hid) in self.pubs


	def publications_count(self):
		return self.pubs.count(self.record_separator)


	@classmethod
	def __to_record_format(cls, tid, hid):
		"""
		Поверне запис, під яким слід зберегти посилання на оголошення.
		"""
		return str(tid) + cls.record_separator + str(hid)


	@staticmethod
	def __to_tid_and_hid(record):
		"""
		Поверне tid та hid оголошення, конвертнувши їх із запису record.
		"""
		tid, hid = record.split(':')
		return int(tid), int(hid)

