#coding=utf-8
import MySQLdb
from celery import Task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from core.publications.constants import OBJECTS_TYPES

from core.publications.models import HousesHeads
from core.publications.objects_constants.houses import HOUSE_SALE_TYPES
from core.search.utils import sale_terms_index_data, living_rent_terms_index_data
from mappino.celery import app


class SphinxUpdateIndexTask(Task):
	"""
	Базовий клас для всіх задач, пов’язаних зі sphinx’ом.
	Кешує з’єднання із searchd для повторного використання під час наступного запуску задачі.
	"""
	abstract = True
	ignore_result = True
	max_retries = 1

	connection = None


	def connect(self):
		self.connection = MySQLdb.connect(
			host = settings.SPHINX_SEARCH['HOST'],
			port = settings.SPHINX_SEARCH['PORT'],
		)

	@property
	def cursor(self):
		if self.connection is None:
			self.connect()
			return self.connection.cursor
		else:
			return self.connection.cursor


	def update_index(self, tid, hid, title, description, sale_terms, rent_terms, location=None, other=None):
		if location is None:
			location = ''
		if other is None:
			other = ''


		def execute():
			self.cursor().execute(u"""
				REPLACE INTO publications_rt (
					id, title, description, sale_terms, rent_terms, location, other, tid, hid)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", [
				int(tid) * int(hid) + int(tid),
				title, description, sale_terms,
				rent_terms, location, other, tid, hid
			])

		try:
			execute()
		except MySQLdb.OperationalError:
			# Якщо втрачено з’єднання - спробувати повторно з’єднатись.
			# OperationalError може свідчити і про інші помилки,
			# тож не варто перехоплювати дану викл. ситуацію більше одного разу.
			self.connect()
			execute()



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_house_index(self, hid):
	try:
		try:
			head = HousesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise self.Reject(e, requeue=False)


		#-- sale terms
		sale_terms_idx = sale_terms_index_data(head)
		# дім має додаткове поле в умовах продажу
		sale_type_idx = u'весь дом'
		if head.sale_terms.sale_type_sid == HOUSE_SALE_TYPES.part():
			sale_type_idx = u'часть дома'
		sale_terms_idx += sale_type_idx


		#-- rent terms
		rent_terms_idx = living_rent_terms_index_data(head)
		# дім має декілька додаткових полів в умовах продажу
		if head.rent_terms.furniture:
			rent_terms_idx += u'мебель'
		if head.rent_terms.refrigerator:
			rent_terms_idx += u'холодильник'
		if head.rent_terms.tv:
			rent_terms_idx += u'телевизор'
		if head.rent_terms.washing_machine:
			rent_terms_idx += u'стиральная машина'
		if head.rent_terms.conditioner:
			rent_terms_idx += u'кондиционер'
		if head.rent_terms.home_theater:
			rent_terms_idx += u'домашний кинотеатр'


		self.update_index(
			tid = OBJECTS_TYPES.house(),
			hid = hid,
			title = head.body.title,
		    description = head.body.description,
		    sale_terms = sale_terms_idx,
		    rent_terms = rent_terms_idx
		)
	except Exception as e:
		self.retry(exc=e)