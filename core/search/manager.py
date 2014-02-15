#coding=utf-8
import MySQLdb
from django.conf import settings
from core.publications.constants import OBJECTS_TYPES
from core.publications.models_signals import updated as publication_model_updated
from core.search.tasks import update_house_index
from mappino.celery import app
from mappino.wsgi import redis_connections



class SearchManager(object):
	def __init__(self):
		self.redis = redis_connections['cache']
		self.prefix = 'search_idx_task_'
		# self.update_interval = 60 * 3 # secs
		self.update_interval = 1 # secs

		self.cursor = None
		self.__reconnect_to_sphinx()

		publication_model_updated.connect(self.model_updated)



	def model_updated(self, **kwargs):
		try:
			tid = kwargs['tid']
			hid = kwargs['hid']
			key = self.task_digest(tid, hid)

			# Якщо в черзі вже зареєстровано запит на зміну даного оголошення - зняти задачу,
			# оскільки є вірогідність, що користувач продовжить редагувати оголошення,
			# а це, в свою чергу, спричинить небажану багаторазову перебудову індекса.
			task_id = self.redis.get(key)
			if task_id is not None:
				app.control.revoke(task_id)

			# Зареєструвати нову відкладену задачу на оновлення індекса
			if tid == OBJECTS_TYPES.house():
				task = update_house_index.apply_async([hid, ], countdown=self.update_interval)
			else:
				# todo
				raise Exception('Todo')

			pipe = self.redis.pipeline()
			pipe.set(key, task.id)
			pipe.expire(key, self.update_interval)
			pipe.execute()
		except Exception:
			# Всі виключні ситуації подавляються умисно.
			# Таким чином, навіть якщо celery чи sphinx відпадуть - це ніяк не вплине на роботу інших,
			# пов’язаних із цією підсистем і запит принаймні виконається.
			# Про виключні ситуації в даному модулі слід повідомляти в лог або адмінам на email.
			# todo: add log record here or email
			pass


	def task_digest(self, tid, hid):
		return self.prefix + unicode(tid) + ':' +  unicode(hid)


	def process_search_query(self, query, user_id):
		def execute():
			self.cursor.execute(u"SELECT tid, hid FROM publications_rt "
			                "WHERE MATCH('{query}') AND uid = {uid} LIMIT 50".format(
				query = query, uid = user_id))

			results = {}
			for record in self.cursor.fetchall():
				tid = record[0]
				hid = record[1]

				if tid in results:
					results[tid].append(hid)
				else:
					results[tid] = [hid]
			return results

		try:
			return execute()
		except MySQLdb.OperationalError:
			# Якщо втрачено з’єднання - спробувати повторно з’єднатись.
			# OperationalError може свідчити і про інші помилки,
			# тож не варто перехоплювати дану викл. ситуацію більше одного разу.
			self.__reconnect_to_sphinx()
			return execute()



	def __reconnect_to_sphinx(self):
		self.cursor = MySQLdb.connect(
			host = settings.SPHINX_SEARCH['HOST'],
			port = settings.SPHINX_SEARCH['PORT'],
		).cursor()