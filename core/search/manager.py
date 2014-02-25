#coding=utf-8
import Queue

import MySQLdb
from django.conf import settings

from core.publications.constants import OBJECTS_TYPES
from core.publications.models_signals import record_updated
from core.search.tasks import update_house_index, update_flat_index, update_apartments_index, update_dacha_index, \
	update_cottage_index, update_room_index, update_trade_index, update_office_index, update_warehouse_index, \
	update_business_index, update_catering_index, update_garage_index, update_land_index
from mappino.celery import app
from mappino.wsgi import redis_connections



class SearchManager(object):
	def __init__(self):
		self.redis = redis_connections['cache']
		self.prefix = 'search_upd_idx_task_'
		self.update_interval = 60 * 2 # in seconds

		self.connections = Queue.Queue()
		for i in xrange(settings.ESTIMATE_THREADS_COUNT):
			self.connections.put(self.__new_connection())

		record_updated.connect(self.update_record_index)


	def update_record_index(self, **kwargs):
		try:
			tid = kwargs['tid']
			hid = kwargs['hid']
			key = self.__task_digest(tid, hid)

			# Якщо в черзі вже зареєстровано запит на зміну даного оголошення - зняти задачу,
			# оскільки є вірогідність, що користувач продовжить редагувати оголошення,
			# а це, в свою чергу, спричинить небажану багаторазову перебудову індекса.
			task_id = self.redis.get(key)
			if task_id is not None:
				app.control.revoke(task_id)

			# Зареєструвати нову відкладену задачу на оновлення індекса
			if tid == OBJECTS_TYPES.house():
				task = update_house_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.flat():
				task = update_flat_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.apartments():
				task = update_apartments_index().apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.dacha():
				task = update_dacha_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.cottage():
				task = update_cottage_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.room():
				task = update_room_index.apply_async([hid, ], countdown=self.update_interval)

			elif tid == OBJECTS_TYPES.trade():
				task = update_trade_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.office():
				task = update_office_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.warehouse():
				task = update_warehouse_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.business():
				task = update_business_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.catering():
				task = update_catering_index.apply_async([hid, ], countdown=self.update_interval)

			elif tid == OBJECTS_TYPES.garage():
				task = update_garage_index.apply_async([hid, ], countdown=self.update_interval)
			elif tid == OBJECTS_TYPES.land():
				task = update_land_index.apply_async([hid, ], countdown=self.update_interval)
			else:
				raise ValueError('Invalid @tid')

			pipe = self.redis.pipeline()
			pipe.set(key, task.id)
			pipe.expire(key, self.update_interval)
			pipe.execute()
		except Exception as e:
			# Всі виключні ситуації подавляються умисно.
			# Таким чином, навіть якщо celery чи sphinx відпадуть — це ніяк не вплине на роботу інших,
			# пов’язаних із цією підсистем, і запит принаймні виконається.
			# Про виключні ситуації в даному модулі слід повідомляти в лог або адмінам на email.
			# todo: add log record here or email
			if settings.DEBUG:
				raise e
			pass


	def process_search_query(self, query, user_id):
		query = u"SELECT tid, hid FROM publications_rt " \
		        u"WHERE MATCH('{query}') AND uid = {uid} LIMIT 50".format(
				query = query, uid = user_id)

		results = {}
		for record in self.__execute_query(query):
			tid = record[0]
			hid = record[1]

			if tid in results:
				results[tid].append(hid)
			else:
				results[tid] = [hid]
		return results


	@staticmethod
	def __new_connection():
		return MySQLdb.connect(
			host = settings.SPHINX_SEARCH['HOST'],
			port = settings.SPHINX_SEARCH['PORT'],
		)


	def __execute_query(self, query):
		connection = self.connections.get(block=True)

		def query_results():
			cursor = connection.cursor()
			cursor.execute(query)
			return cursor.fetchall()

		try:
			results = query_results()
		except MySQLdb.OperationalError:
			# Якщо втрачено з’єднання - спробувати повторно з’єднатись.
			# OperationalError може свідчити і про інші помилки,
			# тож не варто перехоплювати дану викл. ситуацію більше одного разу.
			connection = self.__new_connection()
			results = query_results()

		self.connections.put(connection)
		return results


	def __task_digest(self, tid, hid):
		"""
		Повертає унікальний id для запису про те,
		що запит на оновлення індексу вже присутній в черзі
		"""
		return self.prefix + unicode(tid) + ':' +  unicode(hid)