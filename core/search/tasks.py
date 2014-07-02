#coding=utf-8
import MySQLdb
from celery import Task
from celery.exceptions import Reject
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from core.publications.constants import OBJECTS_TYPES
from core.publications.models import HousesHeads, FlatsHeads, ApartmentsHeads, RoomsHeads, CottagesHeads, TradesHeads, \
	OfficesHeads, WarehousesHeads, BusinessesHeads, CateringsHeads, GaragesHeads, LandsHeads
from core.publications.objects_constants.houses import HOUSE_SALE_TYPES
from core.search.utils import sale_terms_index_data, living_rent_terms_index_data, house_body_index_data, \
	flat_body_index_data, apartments_body_index_data, room_body_index_data, commercial_rent_terms_index_data, trades_body_index_data, office_body_index_data, \
	warehouse_body_index_data, business_body_index_data, catering_body_index_data, garage_body_index_data, \
	land_body_index_data
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
	def cursor(self):
		if self.connection is None:
			self.connect()
		return self.connection.cursor()


	def connect(self):
		self.connection = MySQLdb.connect(
			host = settings.SPHINX_SEARCH['HOST'],
			port = settings.SPHINX_SEARCH['PORT'],
		)


	def update_index(self, tid, hid, uid, title, description, sale_terms, rent_terms, location=None, other=None):
		if location is None:
			location = ''
		if other is None:
			other = ''


		def execute():
			cursor = self.cursor()
			cursor.execute(u"""
				REPLACE INTO publications_rt (
					id, title, description, sale_terms, rent_terms, location, other, tid, hid, uid)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", [
				((int(hid) * OBJECTS_TYPES.count) + int(tid)) + 1,
				title, description, sale_terms,
				rent_terms, location, other, tid, hid, uid
			])

		try:
			execute()
		except Exception:
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
			raise Reject(e, requeue=False)

		sale_terms_idx = sale_terms_index_data(head)
		# дім має додаткове поле в умовах продажу
		sale_type_idx = u'весь дом'
		if head.sale_terms.sale_type_sid == HOUSE_SALE_TYPES.part():
			sale_type_idx = u'часть дома'
		sale_terms_idx += sale_type_idx

		self.update_index(
			tid = OBJECTS_TYPES.house(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  house_body_index_data(head.body),
		    sale_terms = sale_terms_idx,
		    rent_terms = living_rent_terms_index_data(head),
		    other='дом, дома, дача, дачи, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_flat_index(self, hid):
	try:
		try:
			head = FlatsHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.flat(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  flat_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = living_rent_terms_index_data(head),
		    other='квартиры, квартира, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_apartments_index(self, hid):
	try:
		try:
			head = ApartmentsHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.apartments(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  apartments_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = living_rent_terms_index_data(head),
		    other='апартаменты, апартамент, ' # type
		)
	except Exception as e:
		self.retry(exc=e)


@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_cottage_index(self, hid):
	try:
		try:
			head = CottagesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		sale_terms_idx = sale_terms_index_data(head)
		# котедж має додаткове поле в умовах продажу
		sale_type_idx = u'весь дом'
		if head.sale_terms.sale_type_sid == HOUSE_SALE_TYPES.part():
			sale_type_idx = u'часть дома'
		sale_terms_idx += sale_type_idx

		self.update_index(
			tid = OBJECTS_TYPES.cottage(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  house_body_index_data(head.body),
		    sale_terms = sale_terms_idx,
		    rent_terms = living_rent_terms_index_data(head),
		    other='коттеджи, коттедж, ' # type
		)
	except Exception as e:
		self.retry(exc=e)

#
# todo: possible deprecated method
# @app.task(bind=True, base=SphinxUpdateIndexTask)
# def update_cottage_index(self, hid):
# 	try:
# 		try:
# 			head = CottagesHeads.by_id(hid, select_body=True)
# 		except ObjectDoesNotExist as e:
# 			raise Reject(e, requeue=False)
#
# 		self.update_index(
# 			tid = OBJECTS_TYPES.cottage(),
# 			hid = hid,
# 		    uid = head.owner.id,
# 			title = head.body.title if head.body.title else u'',
# 		    description = head.body.description if head.body.description else u'' +
# 		                 cottage_body_index_data(head.body),
# 		    sale_terms = sale_terms_index_data(head),
# 		    rent_terms = living_rent_terms_index_data(head)
# 		)
# 	except Exception as e:
# 		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_room_index(self, hid):
	try:
		try:
			head = RoomsHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.room(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  room_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = living_rent_terms_index_data(head),
		    other='комнаты, комната, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_trade_index(self, hid):
	try:
		try:
			head = TradesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.trade(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  trades_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='торговые помещения, торговое помещение, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_office_index(self, hid):
	try:
		try:
			head = OfficesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.office(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  office_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='офис, офисы, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_warehouse_index(self, hid):
	try:
		try:
			head = WarehousesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.warehouse(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  warehouse_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='склад, склады, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_business_index(self, hid):
	try:
		try:
			head = BusinessesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.business(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  business_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='готовый бизнес, готовые бизнесы, бизнес, бизнесы, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_catering_index(self, hid):
	try:
		try:
			head = CateringsHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.catering(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  catering_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='общепит, общепиты, питание, питания, общественные, общественного, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_garage_index(self, hid):
	try:
		try:
			head = GaragesHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.garage(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  garage_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='гараж, гаражи, ' # type
		)
	except Exception as e:
		self.retry(exc=e)



@app.task(bind=True, base=SphinxUpdateIndexTask)
def update_land_index(self, hid):
	try:
		try:
			head = LandsHeads.by_id(hid, select_body=True)
		except ObjectDoesNotExist as e:
			raise Reject(e, requeue=False)

		self.update_index(
			tid = OBJECTS_TYPES.land(),
			hid = hid,
		    uid = head.owner.id,
			title = head.body.title if head.body.title else u'',
		    description = head.body.description if head.body.description else u'' +
		                  land_body_index_data(head.body),
		    sale_terms = sale_terms_index_data(head),
		    rent_terms = commercial_rent_terms_index_data(head),
		    other='земельные участки, земельный участок, земля, ' # type
		)
	except Exception as e:
		self.retry(exc=e)